CREATE TABLE WRLDC_REST_SUBSET.USER_LOGIN (
	id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
    user_id NUMBER(5)  NOT NULL,
    password VARCHAR2(10)  NOT NULL,
    role VARCHAR2(1)  NOT NULL,
    UNIQUE(user_id)
);