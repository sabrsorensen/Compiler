program sample1;
  var i, j: integer;
begin
  read(i); { get i }
  j := 9 + i * 8{.1e-1 issue with this bit}; { evaluate j }
  str := 9;
  write( str );
  write( j ); { print j }
  writeln;
end.