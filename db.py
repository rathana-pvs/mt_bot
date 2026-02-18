import os

from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

# 1. Get the directory where THIS db.py file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Join it with the filename to create an absolute path
# This ensures it's always /home/rathana/PycharmProjects/trading_bot/trading_bot.db
DB_PATH = os.path.join(BASE_DIR, 'trading_bot.db')

db = SqliteDatabase(DB_PATH)


class BotConfig(Model):
    acc_id = CharField(primary_key=True)
    name = CharField()
    pair = CharField()
    lot_size = FloatField()
    grid_step = IntegerField()
    tp = FloatField()
    max_position = IntegerField()
    active = IntegerField(default=1)
    # updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class BotLog(Model):
    id = PrimaryKeyField()
    acc_id = ForeignKeyField(BotConfig, on_delete='CASCADE', unique=True)
    log = TextField()
    class Meta:
        database = db

    @classmethod
    def update_log(cls, acc_id, log_message):
        (cls.insert(acc_id=acc_id, log=log_message)
         .on_conflict(
            conflict_target=[cls.acc_id],
            update={cls.log: log_message}
        ).execute())

    @classmethod
    def get_log(cls, acc_id=None):
        if not acc_id:
            return ""

        bot = cls.get_or_none(BotLog.acc_id == str(acc_id).strip())
        return bot.log if bot else ""


db.connect()
db.create_tables([BotConfig, BotLog])
BotConfig.get_or_create(
        acc_id='rn-gold',
        defaults={'name': 'Rathana Gold', 'pair': 'XAUUSDm', 'lot_size': 0.01, 'grid_step': 10, 'tp': 20, 'max_position': 100, 'active': 1}
    )

def find_by_acc_id(acc_id):
    bot = BotConfig.get_or_none(BotConfig.acc_id == acc_id.strip())
    if bot:
        data = model_to_dict(bot)
        # # Convert the datetime object to a string format JSON understands
        # if data.get('updated_at'):
        #     data['updated_at'] = data['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        return data

    return None

def update_existing_bot(payload):
    # 1. Extract the acc_id to use in the WHERE clause
    # We use .pop() so acc_id isn't in the data we try to "SET"
    data = payload.copy()
    target_id = data.pop('acc_id', None)
    print(data)
    bot = BotConfig.get_or_none(BotConfig.acc_id == target_id.strip())
    if target_id is None:
        print("Error: No acc_id provided in payload")
        return

    # 2. Perform the update
    # Peewee's .update(**data) matches keys to columns automatically
    query = BotConfig.update(**data).where(BotConfig.acc_id == target_id.strip())
    rows_affected = query.execute()

    if rows_affected == 0:
        print(f"Update skipped: Account {target_id} not found in database.")
    else:
        print(f"Success: Updated Account {target_id}.")



