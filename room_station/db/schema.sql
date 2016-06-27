CREATE TABLE CALENDAR(
	CODE CHAR(24),
	ORA CHAR(10),
	MESSAGE CHAR(40) NOT NULL,
	PRIORITY CHAR(1) NOT NULL,
	PRIMARY KEY(CODE)
);

CREATE TABLE CODE(
  CODE CHAR(6),
  PRIMARY KEY(CODE)
)