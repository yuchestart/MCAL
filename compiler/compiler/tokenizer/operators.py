OPERATOR_LIST =\
"""=
+=
-=
*=
/=
%=
+
-
*
/
%
==
!=
&&
||
!
&
<
>
<=
>=
:
?""".split("\n")
OPERATORS = r"|".join(map(lambda x: "".join(map(lambda y: "\\"+y,x)), OPERATOR_LIST))