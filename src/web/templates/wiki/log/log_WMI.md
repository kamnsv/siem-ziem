![logo](/static/images/logo.png)

##  Настройка WMI

Описание процесса настройки источников для отправки сообщений в ZIEM  
Область применения:  
> Для устройств, способные генерировать события по технологии `WMI`  

##### Содержание  
[Описание](#inf)  
[Настройки](#opt)  
[Алгоритм](#alg)

<a name="inf"/>  
## Описание  
</a>  

Технология WMI — это расширенная и адаптированная под Windows реализация стандарта WBEM (на англ.), принятого многими компаниями, в основе которого лежит идея создания универсального интерфейса мониторинга и управления различными системами и компонентами распределённой информационной среды предприятия с использованием объектно-ориентированных идеологий и протоколов HTML и XML.

Одной из наиболее мощных возможностей WMI является так называемая подписка на извещения о событиях WMI. 

При наступлении события WMI автоматически создаёт экземпляр класса, которому соответствует это событие.

Для подписки на извещения о внутренних событиях применяются запросы специального вида на языке WMI Query Language (WQL).

<hr class="pagebreak">

<a name="opt"/>  
## Настройки  
</a>  

**На источнике**

Настраиваются `учетные записи` для чтения журналов через WMI для подключения.

> WMI – это протокол прикладного уровня, работающий поверх DCOM. Соответственно, открывать порты необходимо именно для DCOM, каких-либо своих специальных портов у WMI нет. DCOM, в свою очередь, протокол прикладного уровня, работающий поверх удалённого вызова процедур (Remote procedure call, RPC). Вместе связка WMI-DCOM-RPC образует фундамет удалённого управления Windows.

RPC использует порт TCP 135. Программно RPC реализовано как служба «Удалённый вызов процедур (RPC)» или, по короткому имени, RpcSs. Поэтому для открытия RPC необходимо либо целиком открыть порт TCP 135 для входящих соединений, либо, если позволяет межсетевой экран, открыть порт TCP 135 только для службы RpcSs.

**На ZIEM**

* В `логинах` добавляется пользователь с паролем настроенный на источнике.
* Добавляется источник и указывается `IP адрес` (`порт` является стандартным для DCOM-RPC).



* В `журналах` указываются названия журналов для чтения:

> например *Системный журнал Безопасность* `Security`.

<hr class="pagebreak">

<a name="info"/>  
## Алгоритм  
</a>  

* Для всех указаных журналов в настройках формируется запрос на языке WQL вида:

```
select * from __InstanceCreationEvent 
WHERE TargetInstance isa 'Win32_NTLogEvent' and 
    (TargetInstance.LogFile='jurnal_1' OR 
    TargetInstance.LogFile='jurnal_2');
```
где `jurnal_1` и `jurnal_2` наши журналы.

* Осуществляется соединение с DCOM по указанным IP-адресам.
* При появлении изменений в указанных журналах, клиент ZIEM получает сообщение в виде экземпляров объектов WMI.
* Полученное сообщение проходит процесс парсинга: быстрый разбор необработанных пакетов из полученных объектов WMI.
* Далее по основному алгоритму, сообщение попадает в очереди на нормализацию и дальнейшую корреляцию.