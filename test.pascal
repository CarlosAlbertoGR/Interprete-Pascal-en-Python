PROGRAM TestAutomatico;
VAR
    i : INTEGER;
    total : INTEGER;

BEGIN
    i := 1;
    total := 0;

    WHILE i < 5 DO
    BEGIN
        total := total + i; 
        i := i + 1;
    END;

    { Resultado esperado: total = 10 }
END.