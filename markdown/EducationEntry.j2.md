((* if entry.website *))
## <img src="https://www.google.com/s2/favicons?domain=<<entry.website>>" alt="<<entry.institution>>" height="20"/> [<<entry.institution>>](<<entry.website>>), ((* if entry.degree *))<<entry.degree>> in ((* endif *))<<entry.area>>
((* else *))
## <<entry.institution>>, ((* if entry.degree *))<<entry.degree>> in ((* endif *))<<entry.area>>
((* endif *)) 

((* if entry.date_string *))- <<entry.date_string>>
((* endif *))
((* if entry.location *))- <<entry.location>>
((* endif *))
((* for item in entry.highlights *))
- <<item>>
((* endfor *))
