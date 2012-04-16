{ a sample program 2 }
program sample2;
  var i, sum: integer;
  procedure count( n: integer; var sum: integer );
    var i: integer; { local variable }
  begin
    i := 1;
    sum := 0;
    while ( i <= n ) do { set-up the loop }
      begin
        sum := sum + i * 3 div (1 - sum);
        i := i + 1;
       end
  end;
begin
  read(i); { get i }
  count(i, sum); { call count }
  write(sum); { write result }
  {write('HELLO! WORLD');}
end.
