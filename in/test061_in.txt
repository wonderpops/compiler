function raz(a:integer):integer;
   begin
      result:=0;
      while a>0 do
         begin
            a:=a div 10;
            result:=result+1;
         end;
   end;