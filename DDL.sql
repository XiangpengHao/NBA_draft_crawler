CREATE TABLE player_info
(
  ID         INT  NOT NULL
    PRIMARY KEY,
  name       TEXT NOT NULL,
  weight     INT  NULL,
  height     INT  NULL,
  position   TEXT NULL,
  shoots     TEXT NULL,
  born       TEXT NULL,
  college    TEXT NULL,
  nba_debut  TEXT NULL,
  draft_year INT  NULL,
  team       TEXT NULL
);

CREATE TABLE player_career
(
  ID  INT    NOT NULL
    PRIMARY KEY,
  g   DOUBLE NULL,
  pts DOUBLE NULL,
  trb DOUBLE NULL,
  ast DOUBLE NULL,
  fg  DOUBLE NULL,
  fg3 DOUBLE NULL,
  ft  DOUBLE NULL,
  efg DOUBLE NULL,
  per DOUBLE NULL,
  ws  DOUBLE NULL
);
CREATE TABLE player_college
(
  ID   INT    NOT NULL
    PRIMARY KEY,
  fg   DOUBLE NULL,
  `3p` DOUBLE NULL,
  ft   DOUBLE NULL,
  mp   DOUBLE NULL,
  pts  DOUBLE NULL,
  trb  DOUBLE NULL,
  ast  DOUBLE NULL
);
