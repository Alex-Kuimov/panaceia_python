def decl_of_num(n, es):
  n = n % 100
  if n >= 11 and n <= 19:
      s = es[2]
  else:
      i = n % 10
      if i == 1:
          s = es[0]
      elif i in [2, 3, 4]:
          s = es[1]
      else:
          s = es[2]
  return s



















