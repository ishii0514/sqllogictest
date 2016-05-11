drop table slt_summary;
drop table slt_detail;

CREATE TABLE slt_summary (
  day DATE,
  file_name VARCHAR,
  total NUMERIC(33,0),
  skip_case NUMERIC(33,0),
  valid_case NUMERIC(33,0),
  ok_case NUMERIC(33,0),
  ng_case NUMERIC(33,0),
  COMPOUND KEY pk(day,file_name) NOT NULL UNIQUE
);


create table slt_detail (
 day date,
 file_name varchar,
 row_num integer,
 type varchar,
 skipif varchar,
 onlyif varchar,
 test_result varchar,
 test_msg varchar,
 statement varchar
 );
 