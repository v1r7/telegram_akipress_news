from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def upcoming_sender(self, update, contest_list):
        i = 0
        s = ""
        keyboard = []
        keyboard1 = []
        for er in contest_list:
            i = i + 1
            # LIMITING NO OF EVENTS TO 20
            if i == 16:
                break
            parsed_contest = self.contest_parser(er)
            s = s + str(i) + ". " + parsed_contest["title"] + "\n" + "Start:\n" + \
                parsed_contest["start"].replace("T", " ")\
                + " GMT\n" + str(parsed_contest["start1"]).replace("T", " ") + " IST\n" + \
                "Duration: " + str(parsed_contest["duration"]) + "\n" + \
                parsed_contest["host"] + "\n" + parsed_contest["contest"] + "\n\n"
            keyboard1.append(InlineKeyboardButton(str(i), callback_data=str(i)))
            if i % 5 == 0:
                keyboard.append(keyboard1)
                keyboard1 = []
        keyboard.append(keyboard1)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(s + "Select competition number to get notification" + "\n\n",
                                  reply_markup=reply_markup)


for league in leagues:
    inline_array.append(InlineKeyboardButton(league[0], callback_data=league[1]))

keyboard_elements = [[element] for element in inline_array]

keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_elements)


kbs = []
            s = []
            for x in data.values():
                kbs = [InlineKeyboardButton(text=x, callback_data=data[x])]
                s.append(kbs)
                print(s)
                print(x)
keyboard = InlineKeyboardMarkup(inline_keyboard=[kbs])
