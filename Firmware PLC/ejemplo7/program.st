PROGRAM program0
  VAR
    TON0 : TON;
  END_VAR
  VAR
    I1 AT %IX0.1 : BOOL;
    Q1 AT %QX0.1 : BOOL;
  END_VAR

  TON0(IN := I1, PT := T#3000ms);
  Q1 := TON0.Q;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
