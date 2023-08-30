from bokeh.models import *
from datetime import datetime, timedelta

class TimeSeriesControls:

    def foo(self):
        self.update_freqeuncy = Select(
            title='Update Frequency',
            value='Daily',
            options=['1 minute', '1 hour', 'Daily']
        )

        self.start = DatePicker(
            title='Start',
            value=datetime.date(datetime.now()) - timedelta(days=1),
            min_date="2019-08-01T09:00:00",
            max_date=datetime.date(datetime.now())
        )

        self.end = DatePicker(
            title='End',
            value=datetime.date(datetime.now()),
            min_date="2019-08-01T09:00:00",
            max_date=datetime.date(datetime.now())
        )




        pass




    pass