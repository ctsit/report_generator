
/*
Configure the sqlite prompt 
===================
echo '.mode column'    >  ~/.sqliterc
echo '.header on'      >> ~/.sqliterc
echo '.nullvalue NULL' >> ~/.sqliterc
*/

SELECT * FROM Project;
/*
prjID       prjName     prjDisplayName  prjCretedTime
----------  ----------  --------------  -------------------
1           HCV-TARGET  HCV             2014-12-03 20:27:08
2           Project B                   2014-12-03 20:27:08
*/

SELECT * FROM Site;
/*
siteID      prjID       siteName
----------  ----------  ----------
1           1           UF Site
*/

SELECT * FROM Form;
/*
frmID       frmName       frmCreatedTime
----------  ------------  -------------------
1           demographics  2014-12-03 20:29:55
2           cbc           2014-12-03 20:29:55
*/

SELECT * FROM SiteRun;
/*
srID        siteID      srStartedTime        srFinishedTime
----------  ----------  -------------------  --------------
1           1           2014-12-03 20:51:36  NULL
*/


-- Show site runs
SELECT * FROM Project NATURAL JOIN Site NATURAL JOIN SiteRun ORDER BY siteName, srDate;

-- Query to show form counts for every subject 
SELECT
   prjName, siteName, siteID, srID, srDate, frmName, srdSubjectID, srdFormCount
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   JOIN SiteRunData USING (srID)
   JOIN Form USING (frmID)
WHERE
   srDate > '2014-01-01'
;
/*
prjName     siteName    srDate      frmName       srdSubjectID  srdFormCount
----------  ----------  ----------  ------------  ------------  ------------
HCV-TARGET  UF Site     2014-12-03  demographics  001           1
HCV-TARGET  UF Site     2014-12-03  demographics  002           1
HCV-TARGET  UF Site     2014-12-03  cbc           001           11
HCV-TARGET  UF Site     2014-12-03  cbc           002           12
HCV-TARGET  UF Site     2014-12-03  cbc           003           13
*/

-- Query to show counts groupped by form
SELECT
   prjName, siteName, siteID, srID, srDate, frmName
   , SUM(srdFormCount) AS formCount
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   JOIN SiteRunData USING (srID)
   JOIN Form USING (frmID)
WHERE
   srDate > '2014-01-01'
GROUP BY
   siteName, srDate, frmName
;
/*
prjName     siteName    srDate      frmName     formCount
----------  ----------  ----------  ----------  ----------
HCV-TARGET  UF Site     2014-12-03  cbc         36
HCV-TARGET  UF Site     2014-12-03  demographi  2
*/
