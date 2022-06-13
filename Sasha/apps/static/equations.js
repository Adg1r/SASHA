function kvadrt()
{
d=document
var a = Number(d.form1.num1.value)//для поля ввода a
var b = Number(d.form1.num2.value)//для поля ввода b
var c = Number(d.form1.num3.value)//для поля ввода c
var diz = eval(Math.pow(b,2)-4*a*c)//расчёт дискримина́нта
var e = eval((-b+Math.sqrt(diz))/(2*a))// расчёт если дискр. > 0 для х1
var e1 = eval((-b-Math.sqrt(diz))/(2*a))//расчёт если дискр. > 0 для х2
var e2 = eval(- c/b)//расчёт если a=0, b и c !=0
var e3 = eval(-b/2*a)//расчёт если дискр.=0
var x1 = Number(d.form1.x1.value)//для поля вывода х1
var x2 = Number(d.form1.x2.value)//для поля вывода х2
if(a==0 && b==0 && c==0)
{
x1 = "Любое число";
x2 = "Любое число";
}
else
if(a==0 && b==0 && c!=0)
{
x1 = "Решения нет";
x2 = "Решения нет";
}
else
if(a==0 && b!=0 && c!=0)
{
x1 =eval(e2);
x2 =" ";
}
else
if(a!=0 && diz>0)
{
x1=eval(e);
x2=eval(e1);
}
else
if(a!=0 && diz==0)
{
x1=eval(e3);
x2=" ";
}
else
{
x1 = "Решения нет";
x2 = "Решения нет";
}
d.form1.x1.value=x1;
d.form1.x2.value=x2;
}