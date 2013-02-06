#!/usr/bin/ruby

str = ""
ARGV.each { |nazwa_pliku|
        str += File.open(nazwa_pliku).read()
}

str.scan( /\<([A-Za-z_]+)\/{0,1}\>+|&([A-Za-z_]+);/i).uniq.each { |x| 

         if !x[0].nil? then 
                puts x[0] 
        end  
       
        if !x[1].nil? then 
                puts x[1]
        end 
        
}
