
-- ===================
-- Project
INSERT INTO Project (prjName, prjDisplayName) VALUES
   ('HCVTARGET', 'HCV'),
   ('Project B', 'B'),
   ('Project C', 'C')
;


-- ===================
-- Site
INSERT INTO Site
   (prjID, siteName)
SELECT
   prjID, 'UF'
FROM
   Project
WHERE
   prjName = 'HCVTARGET'
;
INSERT INTO Site
   (prjID, siteName)
SELECT
   prjID, 'Michigan'
FROM
   Project
WHERE
   prjName = 'HCVTARGET'
;
INSERT INTO Site
   (prjID, siteName)
SELECT
   prjID, 'UPenn'
FROM
   Project
WHERE
   prjName = 'HCVTARGET'
;
INSERT INTO Site
   (prjID, siteName)
SELECT
   prjID, 'Chicago'
FROM
   Project
WHERE
   prjName = 'HCVTARGET'
;


-- ===================
-- Form
INSERT INTO Form
   (frmName)
VALUES
   ('demographics'), ('cbc'), ('chemistry'), ('leukocytes')
;

-- ===================
-- SiteRun
INSERT INTO SiteRun
   (siteID, srDate)
SELECT
   siteID, datetime('now')
FROM
   Project
   JOIN Site USING(prjID)
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN ('UF', 'UPenn', 'Chicago', 'Michigan') 
;

INSERT INTO SiteRun
   (siteID, srDate)
SELECT
   siteID, datetime('now', '-1 month')
FROM
   Project
   JOIN Site USING(prjID)
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'UPenn', 'Michigan')
;

INSERT INTO SiteRun
   (siteID, srDate)
SELECT
   siteID, datetime('now', '-2 month')
FROM
   Project
   JOIN Site USING(prjID)
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'UPenn', 'Michigan')
;


INSERT INTO SiteRun
   (siteID, srDate)
SELECT
   siteID, datetime('now', '-7 day')
FROM
   Project
   JOIN Site USING(prjID)
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN ('UF', 'Michigan', 'UPenn', 'Chicago')
;

INSERT INTO SiteRun
   (siteID, srDate)
SELECT
   siteID, datetime('now', '-15 day')
FROM
   Project
   JOIN Site USING(prjID)
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN ('UF', 'Michigan', 'UPenn', 'Chicago')
;



-- ===================
-- SiteRunData

-- two `demographics` forms 
INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '001', 1
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN ('UF', 'UPenn', 'Michigan')
   AND frmName IN( 'demographics', 'leukocytes')
;
  
INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '002', 1
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Michigan', 'UPenn', 'Chicago')
   AND frmName = 'demographics'
;

-- three `cbc` subjects
INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '001', 11
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Michigan', 'Chicago')
   AND frmName = 'cbc'
;

INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '002', 12
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Chicago')
   AND frmName = 'cbc'
;
 
INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '003', 13
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Michigan', 'UPenn', 'Chicago')
   AND frmName = 'cbc'
;

INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '004', 1
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Michigan', 'UPenn', 'Chicago')
   AND frmName IN ('cbc', 'chemistry')
;


INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '100', 1
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Michigan', 'UPenn', 'Chicago')
   AND frmName = 'cbc'
   AND srID IN (1, 2, 3, 4, 14 ) 
;

INSERT INTO SiteRunData
   (srID, frmID, srdSubjectID, srdFormCount)
SELECT
   srID, frmID, '101', 1
FROM
   Project
   JOIN Site USING (prjID)
   JOIN SiteRun USING (siteID)
   LEFT JOIN Form
WHERE
   prjName = 'HCVTARGET'
   AND siteName IN( 'UF', 'Michigan', 'Chicago', 'UPenn')
   AND frmName = 'cbc'
   AND srID IN (1, 2, 4, 7, 14, 15, 18 )
;
