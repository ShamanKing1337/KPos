# KPos

Добрый день!
 
Давайте делать сервер сообщений. 

    Можно на Python/C++/Java
    Нужна полноценная библиотека, которую можно было бы присоединять к любому проекту и далее достаточно было бы обращаться к серверу сообщений указав только его адрес
    Нужно несколько основных Нфункций для библиотеки:
        Отправка сообщений (Send(«MyQueue», message, priority:3, expirationTime:30sec)
        Создание очереди по имени (Create(«MyQueue», persistance:false))
        Ожидание приёма сообщения (Recieve<MyType>())
        Удаление очереди
    Дополнительные функции у самой очереди:
        У каждого сообщения должен быть приоритет
        У каждого сообщения должно быть время жизни
        Очередь должна создаваться «персистентной» или нет. Если остановить сервер очередей сообещений, то персистентные очереди должны сохранить свои сообщения после повторного запуска




Никита! Крч
Нужно все мои функции вынести в динамическую библиотеку! Но меня очень пугает его задание с функцией отправки сообщения, у меня в проге не просит ни приоритет, ни время жизни(но его можно указать вручную в одной из функций, сам увидишь). Тут надо поработать, разобраться в проге, и могу сказать, что внутри проги есть 

1.Создание персистентной очереди(но это одна строка, это меня смущает) (сервер)(ее надо вынести в отдельную функцию)

2. Ожидание приема сообщений(отдельная функция для отдельного потока) (клиент)

3. Удаление очреди (пару строк(/clear))(сервер)(вынести в отдельную функцию)

Значит остается функция отправки сообщения, она как бы есть, но это просто sendto, только ткт опять же повторяюсь не указывается время жизни и приоритет(думаю, на это можно закрыть глаза).

Тут только что до меня дошло, что нужно еще блять делать выбор для создания либо персистетной очереди либо для обычной(у меня в проге персистентная очередь конфликтует с библиотекой обычной очереди, поэтому я использовал дек(увидишь)). Но думаю и тут можно закрыть глаза и создавать всегда персистентную очередь, все равно же есть функция удаления, которая может ее очистить.

Дальше пункты
У каждого сообщения должно быть время жизни(ты увидишь все в комментах проги, но могу сказать, что иногда, в очень редких случаях прога может из-за этого подлагивать)(также для времени жизни я использовал обычное время т.е. 23.09.30   23 часа 9 минут 30 секунд оно у меня представляется интовым числом 230930 и по нему сравнивал время отправки сообщения с настоящим временем НО если время станет 01.00.00 тип час ночи, то он не станет удлаять т.к. 010000 - 230930 вообще нахуй отрицательное время) Но опять же на это глаза можно закрыть.

Про персистентность выше уже говорил.

И самое главное прошу тебя разберись с приоритетом сообщений, всю работу с ними оставляю на тебя, потому что я не вдупляю нахуя это нужно.......................................
