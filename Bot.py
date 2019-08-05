import variable as vrb
import requests

class MyFirstBot:
    #money
    usd = vrb.money['usd']
    eur = vrb.money['eur']
    url_money=vrb.url_money
    all_rates=vrb.all_rates

    #bot
    upd = vrb.methods['updates']
    send = vrb.methods['send']
    tel_api_url=vrb.tel_api_url

    def __init__(self,bot_token=None,text=''):
        self.token=bot_token
        self.text=text



    #Update
    def get_updates(self):
        res=requests.get(self.tel_api_url.format(self.token)+self.upd)
        return res.json()
        pass



    #Get ID
    def get_chat_id(self):
        return self.get_updates()['result'][-1]['message']['chat']['id']
        pass



    #Get last Message
    def get_last_message(self):
        return self.get_updates()['result'][-1]['message']['text']
        pass




    #Help
    def bot_help(self):
        if(self.get_last_message()=='/help'):
            message= 'Вывод курса валют:\n' \
                   '/money [валюта] (usd, eur) \n' \
                   '/money'
            return self.send_message(message)


        elif(self.get_last_message()=='/money'):
            return self.print_rates()

        elif(self.get_last_message()=='/money/usd'):
            return self.send_message(self.print_money(self.usd))

        elif (self.get_last_message() == '/money/eur'):
            return self.send_message(self.print_money(self.eur))

        else:
            return 'Команды: /help'



    #Update money
    def get_update_money(self,money):
        res=requests.get(self.url_money.format(money))
        return res.json()
        pass




    #Money
    def print_money(self, valiuta):
        date=self.get_update_money(valiuta)['Date']
        name = self.get_update_money(valiuta)['Cur_Name']
        rate = self.get_update_money(valiuta)['Cur_OfficialRate']
        return 'За {}, курс {}, за 1 {}'.format(date, rate, name)





    #Get Rates
    def get_rates_money(self):
        res=requests.get(self.all_rates)
        return res.json()
        pass




    #Print Rates
    def print_rates(self):
        rates=[]
        chat_id = self.get_chat_id()
        for i in range(len(self.get_rates_money())):
            date=self.get_rates_money()[i]['Date']
            name=self.get_rates_money()[i]['Cur_Name']
            rate=self.get_rates_money()[i]['Cur_OfficialRate']
            text_message = 'За {}, курс {}, за 1 {}'.format(date, rate, name)
            params = {'chat_id': chat_id, 'text': text_message}
            requests.post(self.tel_api_url.format(self.token) + self.send, params)



    #Send Message
    def send_message(self,text):
        chat_id=self.get_chat_id()
        text_message=text
        params={'chat_id':chat_id,'text':text_message}
        requests.post(self.tel_api_url.format(self.token)+self.send,params)




print(MyFirstBot(vrb.bot_token).bot_help())