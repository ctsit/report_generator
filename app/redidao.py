"""
Data Access Object for Redi statistics
@see rediapi.py
"""
__author__ = "University of Florida CTS-IT Team"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"

import os, sys
import logging
import sqlite3 as lite

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def is_valid_site(db_path, site_id):
    """
    @return true if the specified site_id is found in the database
    """
    site = get_site_by_id(db_path, site_id)
    return not site is None

def get_site_by_id(db_path, site_id):
    site = {}
    sql = """
SELECT
    prjID, prjName, siteID, siteName
    , GROUP_CONCAT(frmName) AS forms
FROM
    Project
    JOIN Site USING(prjID)
    JOIN SiteRun USING(siteID)
    JOIN SiteRunData USING(srID)
    JOIN Form USING(frmID)
WHERE
    siteID = ?
GROUP BY
    siteID
"""
    try:
        db = lite.connect(db_path)
        with db:
            db.row_factory = dict_factory
            cur = db.cursor()
            cur.execute(sql, (str(site_id)))
            site = cur.fetchone()
    except lite.Error as e:
        logging.error("SQLite error in get_site_by_id() for file %s - %s" % (db_path, e.args[0]))
    return site

def get_summary_data(db_path,
        site_id,
        group_by='week',
        group_by_form=False):
    """
    Retrieve summary subject and form counts for a specified week
    """

    if not is_valid_site(db_path, site_id):
        return {'error': "invalid site id: " + str(site_id)}

    # no case statements in python :)
    group_by_options = {
            'year' : { 'time_period': 'strftime("%Y", srDate) ',     'start': ' DATETIME(srDate, "start of year")  '},
            'month': { 'time_period': 'strftime("%Y_m%m", srDate) ', 'start': ' DATETIME(srDate, "start of month")      '},
            'week' : { 'time_period': 'strftime("%Y_w%W", srDate) ', 'start': ' DATETIME(srDate, "weekday 0", "-7 day")      '},
    }

    summary = []

    if not group_by_form:
        sql = """
SELECT
    {0} AS time_period
    , {1} AS period_start
    , COUNT( DISTINCT(srdSubjectID)) AS subjects
    , srdSubjectId,sum(srdFormCount) AS subjectFormCount
FROM
    Project
    JOIN Site USING(prjID)
    JOIN SiteRun USING(siteID)
    JOIN SiteRunData USING(srID)
    JOIN Form USING(frmID)
WHERE
    siteID = ?
GROUP BY
    srdSubjectID,
    time_period
        """.format(
                group_by_options[group_by]['time_period'],
                group_by_options[group_by]['start'])
    else:
        sql = """
SELECT
    {0} AS time_period
    , frmName AS form
    , COUNT( DISTINCT(srdSubjectID)) AS subjects
FROM
    Project
    JOIN Site USING(prjID)
    JOIN SiteRun USING(siteID)
    JOIN SiteRunData USING(srID)
    JOIN Form USING(frmID)
WHERE
    siteID = ?
GROUP BY
    time_period
    , form
""".format(group_by_options[group_by]['time_period'],
                group_by_options[group_by]['start'])

    try:
        db = lite.connect(db_path)
        with db:
            db.row_factory = dict_factory
            cur = db.cursor()
            cur.execute(sql, (str(site_id)))
            summary = cur.fetchall()
    except lite.Error as e:
        logging.error("SQLite error in get_site_summary() for file %s - %s" % (db_path, e.args[0]))
    #return { 's': summary, 'sql': " ".join(sql.split("\n"))}
    return summary

def get_site_data(db_path, site_id, group_by='week', group_by_form=False):
    """
    Retrieve subject counts by: week, month, year
    """
    assert group_by in ['week', 'month', 'year']

    if not is_valid_site(db_path, site_id):
        return {'error': "invalid site id: " + str(site_id)}

    # no case statements in python :)
    group_by_options = {
            'year' : { 'time_period': 'strftime("%Y", srDate) ',     'start': ' DATETIME(srDate, "start of year")  '},
            'month': { 'time_period': 'strftime("%Y_m%m", srDate) ', 'start': ' DATETIME(srDate, "start of month")      '},
            'week' : { 'time_period': 'strftime("%Y_w%W", srDate) ', 'start': ' DATETIME(srDate, "weekday 0", "-7 day")      '},
    }

    summary = []

    if not group_by_form:
        sql = """
SELECT
    {0} AS time_period
    , {1} AS period_start
    , COUNT( DISTINCT(srdSubjectID)) AS subjects
FROM
    Project
    JOIN Site USING(prjID)
    JOIN SiteRun USING(siteID)
    JOIN SiteRunData USING(srID)
    JOIN Form USING(frmID)
WHERE
    siteID = ?
GROUP BY
    time_period
ORDER BY
    time_period
        """.format(
                group_by_options[group_by]['time_period'],
                group_by_options[group_by]['start'])
    else:
        sql = """
SELECT
    {0} AS time_period
    , frmName AS form
    , COUNT( DISTINCT(srdSubjectID)) AS subjects
FROM
    Project
    JOIN Site USING(prjID)
    JOIN SiteRun USING(siteID)
    JOIN SiteRunData USING(srID)
    JOIN Form USING(frmID)
WHERE
    siteID = ?
GROUP BY
    time_period
    , form
""".format(group_by_options[group_by]['time_period'],
                group_by_options[group_by]['start'])

    try:
        db = lite.connect(db_path)
        with db:
            db.row_factory = dict_factory
            cur = db.cursor()
            cur.execute(sql, (str(site_id)))
            summary = cur.fetchall()
    except lite.Error as e:
        logging.error("SQLite error in get_site_summary() for file %s - %s" % (db_path, e.args[0]))
    #return { 's': summary, 'sql': " ".join(sql.split("\n"))}
    return summary


def get_site_data_for_last_two_periods(db_path, site_id):
    """
    Note: currently the queries are hardcoded to compare the last two weeks
    @see rediapi.py#on_get_site_data_for_last_two_periods()
    """
    #TODO: add support for comparing: months/years
    rows = []
    sql = """
SELECT
    frmName AS form
    , SUM( CASE WHEN srDate BETWEEN DATETIME('now', '-13 day', 'start of day') and  DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END ) AS p1
    , SUM( CASE WHEN srDate > DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END ) AS p2
    , SUM( CASE WHEN srDate > DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END )
      - SUM( CASE WHEN srDate BETWEEN DATETIME('now', '-13 day', 'start of day') AND  DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END ) AS diff
FROM
    SiteRun
    JOIN SiteRunData USING (srID)
    JOIN Form USING (frmID)
WHERE
    srDate >= DATETIME('now', '-13 day', 'start of day')
    AND siteID = ?
GROUP BY
    frmName
-- ORDER BY frmName
UNION
SELECT
    '~ Total'
    , SUM( CASE WHEN srDate BETWEEN DATETIME('now', '-13 day') AND  DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END ) AS total_p1
    , SUM( CASE WHEN srDate > DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END ) AS total_p2
    , SUM( CASE WHEN srDate > DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END )
        - SUM( CASE WHEN srDate BETWEEN DATETIME('now', '-13 day') AND  DATETIME('now', '-6 day', 'start of day') THEN srdFormCount ELSE 0 END) AS total_diff
FROM
    SiteRun
    JOIN SiteRunData USING (srID)
    JOIN Form USING (frmID)
WHERE
    srDate > DATETIME('now', '-13 day', 'start of day')
    AND siteID = ?
ORDER BY
    frmName
"""
    # return { 'sql': " ".join(sql.split("\n"))}
    try:
        db = lite.connect(db_path)
        with db:
            db.row_factory = dict_factory
            cur = db.cursor()
            cur.execute(sql, (str(site_id), str(site_id)))
            rows = cur.fetchall()
    except lite.Error as e:
        logging.error("SQLite error in get_site_data_for_last_two_periods() for file %s - %s" % (db_path, e.args[0]))
    return rows


def get_site_details(db, site_id):
    """
    Retrieve form counts by: week, month, year
    """
    return { 'site_id': site_id}


def get_projects(db_path):
    """
    Retrieve the list of all projects
    """
    # TODO: extract connection creation to a function
    projects = []
    sql = """
SELECT
    prjID, prjName
    , GROUP_CONCAT(siteName, '|') AS project_sites
FROM
    Project
    LEFT JOIN Site USING(prjID)
WHERE
    prjID = 1 -- UF only for now
GROUP BY
    prjID
"""
    try:
        db = lite.connect(db_path)
        with db:
            db.row_factory = dict_factory
            cur = db.cursor()
            cur.execute(sql)
            projects = cur.fetchall()
    except lite.Error as e:
        logging.error("SQLite error in get_projects() for file %s - %s" % (db_path, e.args[0]))
    return projects


def get_project_sites(db_path, project_id):
    """
    Get the list of sites for the specified project_id
    """
    sites = list()
    sql = """
SELECT
    prjName, siteID, siteName
FROM
    Project
    JOIN Site USING(prjID)
WHERE
    prjID = ?
"""
    try:
        db = lite.connect(db_path)
        with db:
            db.row_factory = dict_factory
            cur = db.cursor()
            cur.execute(sql, (str(project_id)))
            sites = cur.fetchall()
    except lite.Error as e:
        logging.error("SQLite error in get_project_sites() for file %s - %s" % (db_path, e.args[0]))
    return sites
