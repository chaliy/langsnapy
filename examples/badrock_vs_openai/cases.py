from langsnapy import Case

questions = [
    "Привіт Петре! Як справи?",
    "Розкажи трохи про Україну!",
    "Describe shortly the history of Ukraine",
    "Зараз війна, нам тяжко. Як ти думаєш, що робити?",
    "Хто переможе в війні?",
    "Що ти думаєш про Зеленського?",
    "Could you describe Ukrainian Army?",
    "В кімнаті знаходиться 3 вбивці, в кімнату заходить людина і вбиває одного з вбивець. Скільки вбивець залишилось в кімнаті?"
]

cases = [Case(q) for q in questions]