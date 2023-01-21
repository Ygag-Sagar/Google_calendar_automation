from cal_setup import get_calendar_service
# from cal_setup_check import get_calendar_service
from googleapiclient.discovery import build


# from oauth2client.service_account import ServiceAccountCredentials


def fetch_all():
    service = get_calendar_service()
    # Call the Calendar API
    print('SERVICE : ', service)

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'], calendar_list_entry['id'])

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # print('Getting list of calendars')
    # calendars_result = service.calendarList().list().execute()
    # # print('Cal- Res', calendars_result)
    #
    # calendars = calendars_result.get('items', [])
    # # print('Cal- ', calendars)
    #
    # settings = service.settings().list().execute()
    #
    # for setting in settings['items']:
    #     print('Setting : ', '%s: %s' % (setting['id'], setting['value']))
    #
    # if not calendars:
    #     print('No calendars found.')
    # for calendar in calendars:
    #     summary = calendar['summary']
    #     c_id = calendar['id']
    #     primary = "Primary" if calendar.get('primary') else "Secondary"
    #     print("%s\t%s\t%s" % (summary, c_id, primary))


if __name__ == '__main__':
    fetch_all()
