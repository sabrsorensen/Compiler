program sample1;
  var i, j: integer;
begin  
  read(i); { get i }
  j := 9 + i * 8.1e-1; { evaluate j }
  write( 'Result is ');
  write( j ); { print j }
  writeln;
end.