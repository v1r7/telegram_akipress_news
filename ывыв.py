for tags in soup[::6]:
	list_of_news_categories.append(tags.text)
list_of_news_categories3 = ''.join(list_of_news_categories).splitlines()
list_of_news_categories5 = list(filter(None, list_of_news_categories3))
print(list_of_news_categories5)
for i in soup[::6]:
	urls.append(i)
print(urls)

bot.edit_message_text(chat_id=call.message.chat.id,
                      message_id=call.message.message_id,
                      text=list_welcome,
                      reply_markup=markup)

print(soup[0].find_all('a'))

cursor.execute("SELECT message,timestamp FROM `logger` WHERE message like '%mp4%' order by timestamp DESC limit 2")
result = cursor.fetchall()
vidlist = ""
for row in result:
		vidlist = vidlist+"[InlineKeyboardButton(text='"+row[0]+"', callback_data='"+str(row[1])+"')],"
vidlist = vidlist+"]"

keyboard = InlineKeyboardMarkup(inline_keyboard=[vidlist])

for x in data.values():
	kbs = kbs + [InlineKeyboardButton(text=x, callback_data=data[x])]
keyboard = InlineKeyboardMarkup(inline_keyboard=[kbs])