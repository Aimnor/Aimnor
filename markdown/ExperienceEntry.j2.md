((* if entry.website *))
## <img src="https://www.google.com/s2/favicons?domain=<<entry.website>>" alt="<<entry.company>>" height="20"/> [<<entry.company>>](<<entry.website>>), <<entry.position>>
((* else *))
## <<entry.company>>, <<entry.position>>
((* endif *)) 

((* if entry.date_string *))- <<entry.date_string>>
((* endif *))
((* if entry.location *))- <<entry.location>>
((* endif *))
((* for item in entry.highlights *))
- <<item>>
((* endfor *))
