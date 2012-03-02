{ a sample program 2 This should break }
program sample2;
  var i, sum: integer;
begin
  read(i) { get i break with no semi-colon}
  count(i, sum); { call count }
  write(sum); { write result }
  writeln;
  write('HELLO! WORLD');
  writeln;
end.
