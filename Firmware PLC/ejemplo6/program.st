PROGRAM program0
  VAR
    CTU0 : CTU;
  END_VAR
  VAR
    I1 AT %IX0.1 : BOOL;
    I2 AT %IX0.2 : BOOL;
    Q1 AT %QX0.1 : BOOL;
  END_VAR
  VAR
    R_TRIG1 : R_TRIG;
  END_VAR

  R_TRIG1(CLK := I1);
  CTU0(CU := R_TRIG1.Q, R := I2, PV := 2);
  Q1 := CTU0.Q;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
