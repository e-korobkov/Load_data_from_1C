
&НаСервере
Процедура ЗаполнитьДанныеОбъекта(Ссылка, Дата)
	
	ИзменяемыйОбъект 							= Ссылка.ПолучитьОбъект();
	ИзменяемыйОбъект.ОбменДанными.Загрузка 		= Истина;
	//ИзменяемыйОбъект.ЛБ_Гуид 					= Строка(Ссылка.УникальныйИдентификатор());
	//ИзменяемыйОбъект.ЛБ_ДатаИзменения 			= Дата;
	ИзменяемыйОбъект.Записать();

КонецПроцедуры

&НаСервере
Процедура ЗаполнитьРеквизитыНаСервере()
	
	ТекДата = ТекущаяДата();
	
	Если Объект.ПерезаполнитьВНоменклатуре = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	Номенклатура.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.Номенклатура КАК Номенклатура";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВЗначенияхСвойствОбъектов = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ЗначенияСвойствОбъектов.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.ЗначенияСвойствОбъектов КАК ЗначенияСвойствОбъектов";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВВидеНоменклатуры = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ВидыНоменклатуры.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.ВидыНоменклатуры КАК ВидыНоменклатуры";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВДопРеквизитах = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ДополнительныеРеквизитыИСведения.Ссылка КАК Ссылка
			|ИЗ
			|	ПланВидовХарактеристик.ДополнительныеРеквизитыИСведения КАК ДополнительныеРеквизитыИСведения";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;

	
	Если Объект.ПерезаполнитьВПартнерах = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	Партнеры.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.Партнеры КАК Партнеры";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВВидахЦен = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ВидыЦен.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.ВидыЦен КАК ВидыЦен";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	
	Если Объект.ПерезаполнитьВПричинахОтменыЗаказовКлиентов = Истина Тогда

		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ПричиныОтменыЗаказовКлиентов.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.ПричиныОтменыЗаказовКлиентов КАК ПричиныОтменыЗаказовКлиентов";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВБизнесРегионах = Истина Тогда

		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	БизнесРегионы.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.БизнесРегионы КАК БизнесРегионы";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВСегментахНоменклатуры = Истина Тогда

		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	СегментыНоменклатуры.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.СегментыНоменклатуры КАК СегментыНоменклатуры";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	
	
	Если Объект.ПерезаполнитьВРегистрацияЦенНоменклатурыПоставщикаПрисоединенныеФайлы = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	РегистрацияЦенНоменклатурыПоставщикаПрисоединенныеФайлы.Ссылка КАК Ссылка
			|ИЗ
			|	Справочник.РегистрацияЦенНоменклатурыПоставщикаПрисоединенныеФайлы КАК РегистрацияЦенНоменклатурыПоставщикаПрисоединенныеФайлы";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВОтчетОРозничныхПродажах = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ОтчетОРозничныхПродажах.Ссылка КАК Ссылка,
			|	ОтчетОРозничныхПродажах.Дата КАК Дата
			|ИЗ
			|	Документ.ОтчетОРозничныхПродажах КАК ОтчетОРозничныхПродажах
			|ГДЕ
			|	ОтчетОРозничныхПродажах.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВКассоваяСмена = Истина Тогда

		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	УдалитьКассоваяСмена.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.УдалитьКассоваяСмена КАК УдалитьКассоваяСмена
			|ГДЕ
			|	УдалитьКассоваяСмена.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВЧекККМ = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ЧекККМ.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.ЧекККМ КАК ЧекККМ
			|ГДЕ
			|	ЧекККМ.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВВозвратТоваровОтКлиента = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ВозвратТоваровОтКлиента.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.ВозвратТоваровОтКлиента КАК ВозвратТоваровОтКлиента
			|ГДЕ
			|	ВозвратТоваровОтКлиента.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВАктВыполненныхРабот = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	АктВыполненныхРабот.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.АктВыполненныхРабот КАК АктВыполненныхРабот
			|ГДЕ
			|	АктВыполненныхРабот.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВРеализацияТоваровУслуг = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	РеализацияТоваровУслуг.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.РеализацияТоваровУслуг КАК РеализацияТоваровУслуг
			|ГДЕ
			|	РеализацияТоваровУслуг.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВЗаказКлиента = Истина Тогда
		
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ЗаказКлиента.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.ЗаказКлиента КАК ЗаказКлиента
			|ГДЕ
			|	ЗаказКлиента.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВСчетНаОплатуКлиенту = Истина Тогда

		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	СчетНаОплатуКлиенту.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.СчетНаОплатуКлиенту КАК СчетНаОплатуКлиенту
			|ГДЕ
			|	СчетНаОплатуКлиенту.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
		
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВПоступлениеБезналичныхДенежныхСредств = Истина Тогда

		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	ПоступлениеБезналичныхДенежныхСредств.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.ПоступлениеБезналичныхДенежныхСредств КАК ПоступлениеБезналичныхДенежныхСредств
			|ГДЕ
			|	ПоступлениеБезналичныхДенежныхСредств.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВСписаниеБезналичныхДенежныхСредств = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	СписаниеБезналичныхДенежныхСредств.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.СписаниеБезналичныхДенежныхСредств КАК СписаниеБезналичныхДенежныхСредств
			|ГДЕ
			|	СписаниеБезналичныхДенежныхСредств.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВУстановкаЦенНоменклатуры = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	УстановкаЦенНоменклатуры.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.УстановкаЦенНоменклатуры КАК УстановкаЦенНоменклатуры
			|ГДЕ
			|	УстановкаЦенНоменклатуры.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
	Если Объект.ПерезаполнитьВРегистрацияЦенНоменклатурыПоставщика = Истина Тогда
		Запрос = Новый Запрос;
		Запрос.УстановитьПараметр("ДатаНачала", 	Объект.Период.ДатаНачала);
		Запрос.УстановитьПараметр("ДатаОкончания", 	Объект.Период.ДатаОкончания);
		Запрос.Текст = 
			"ВЫБРАТЬ
			|	РегистрацияЦенНоменклатурыПоставщика.Ссылка КАК Ссылка
			|ИЗ
			|	Документ.РегистрацияЦенНоменклатурыПоставщика КАК РегистрацияЦенНоменклатурыПоставщика
			|ГДЕ
			|	РегистрацияЦенНоменклатурыПоставщика.Дата МЕЖДУ НАЧАЛОПЕРИОДА(&ДатаНачала, ДЕНЬ) И КОНЕЦПЕРИОДА(&ДатаОкончания, ДЕНЬ)";
		
		Выборка = Запрос.Выполнить().Выбрать();
		
		Пока Выборка.Следующий() Цикл
			
			ЗаполнитьДанныеОбъекта(Выборка.Ссылка, ТекДата);
			
		КонецЦикла;
	КонецЕсли;
	
КонецПроцедуры



&НаКлиенте
Процедура ЗаполнитьРеквизиты(Команда)
	ЗаполнитьРеквизитыНаСервере();
КонецПроцедуры

&НаСервере
Процедура ЗапуститьЗаполнениеРегламентнымЗаданиемНаСервере()
	
	ЛБ_ОбработчикиРегламентныхЗаданий.ДобавитьРегламентноеЗадание();
	
КонецПроцедуры

&НаКлиенте
Процедура ЗапуститьЗаполнениеРегламентнымЗаданием(Команда)
	ЗапуститьЗаполнениеРегламентнымЗаданиемНаСервере();
КонецПроцедуры
