
-- One project can have multiple sites
CREATE TABLE Project (
   prjID INTEGER PRIMARY KEY AUTOINCREMENT,
   prjName TEXT NOT NULL,
   prjDisplayName TEXT NOT NULL,
   prjCreatedTime DATETIME DEFAULT CURRENT_TIMESTAMP,
   UNIQUE (prjName)
);

-- A site is a location where REDI is executed
CREATE TABLE Site (
   siteID INTEGER PRIMARY KEY AUTOINCREMENT,
   prjID INTEGER,
   siteName TEXT NOT NULL,
   FOREIGN KEY (prjID) REFERENCES Project (prjID),
   UNIQUE (prjID, siteName) 
);

-- Every time a new form name is encountered we insert a row in this table
CREATE TABLE Form (
   frmID INTEGER PRIMARY KEY AUTOINCREMENT,
   frmName TEXT NOT NULL,
   frmCreatedTime DATETIME DEFAULT CURRENT_TIMESTAMP,
   UNIQUE (frmName)
);

CREATE TABLE SiteRun (
   srID INTEGER PRIMARY KEY AUTOINCREMENT,
   siteID INTEGER,
   srDate DATE NOT NULL DEFAULT (date('now','localtime')),
   srStartedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   srFinishedTime DATETIME,
   FOREIGN KEY (siteID) REFERENCES Site (siteID)
);

CREATE TABLE SiteRunData (
   srdID INTEGER PRIMARY KEY AUTOINCREMENT,
   srID INTEGER,
   frmID INTEGER,
   srdSubjectID TEXT NOT NULL,
   srdFormCount INTEGER,
   FOREIGN KEY (srID) REFERENCES SiteRun (srID),
   FOREIGN KEY (frmID) REFERENCES Form (frmID),
   UNIQUE(srID, frmID, srdSubjectID)
);

