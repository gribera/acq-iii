PROGRAM program0
  VAR
    SR0 : SR;
  END_VAR
  VAR
    I1 AT %IX0.1 : BOOL;
    I2 AT %IX0.2 : BOOL;
    Q1 AT %QX0.1 : BOOL;
  END_VAR

  SR0(S1 := I1, R := I2);
  Q1 := SR0.Q1;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
