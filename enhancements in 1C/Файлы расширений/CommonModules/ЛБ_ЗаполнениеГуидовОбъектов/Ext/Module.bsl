﻿Процедура ЛБ_ВыполнитьЗаполнениеГуида(Объект) Экспорт
	
	УстановитьПривилегированныйРежим(Истина);
	Объект.ЛБ_Гуид 			= Строка(Объект.Ссылка.УникальныйИдентификатор());
	Если не Объект.ЛБ_Гуид = "00000000-0000-0000-0000-000000000000" Тогда
		Объект.ЛБ_ДатаИзменения 	= ТекущаяДата();
	КонецЕсли;
	УстановитьПривилегированныйРежим(Ложь);
	
КонецПроцедуры
