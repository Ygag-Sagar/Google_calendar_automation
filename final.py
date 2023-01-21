import datetime
import re
import schedule
# from cal_setup_check import get_calendar_service
from cal_setup import get_calendar_service
from datetime import timezone, timedelta


def main():
    service = get_calendar_service()

    cal_id = ('sagar@yougotagift.com',)  # 'athul.v@yougotagift.com',  'ajdal@yougotagift.com'

    for cid in cal_id:
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting List of events')
        events_result = service.events().list(
            calendarId=cid, timeMin=now,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        # print(events)

        if not events:
            print('### No upcoming events found on calendar ID:', cid, '|'
                                                                       ' RunTime : ', datetime.datetime.now().time(),
                  '###')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print('###', event['summary'], '|', 'Cal ID:', cid, '|'
                                                                ' RunTime : ', datetime.datetime.now().time(), '###')

            event_id = event['id']

            # CONDITIONS
            # HRM123 - Sick Leave (India) (First Half-Day)
            # HRM123 - Sick Leave (India) (First Quarter-Day)
            # HRM123 - Earned Leave (India)
            # HRM123 - Earned Leave (India) (First Half-Day)
            # HRM123 - Earned Leave (India) (First Quarter-Day)
            # HRM123 - Compensatory Off (India)
            # HRM123 - Compensatory Off (India) (First Half-Day)
            # HRM123 - Compensatory Off (India) (First Quarter-Day)
            # HRM123 - Work from home (2 days advance only)
            # HRM123 - Work from home (2 days advance only) (First Half-Day)
            # HRM123 - Work from home (2 days advance only) (First Quarter-Day)
            # HRM123 - FOP (For female employees only)
            # HRM123 - FOP (For female employees only) (First Half-Day)
            # HRM123 - FOP (For female employees only) (First Quarter-Day)
            # HRM123 - Restricted Holiday

            # Sick Leave
            sick_all_day = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)]'
            condition_sick_all_day = re.fullmatch(sick_all_day, event['summary'])

            sick_first_half = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)][ ]' \
                              '[(][F][i][r][s][t][ ][H][a][l][f][-][D][a][y][)]'
            condition_sick_first_half = re.fullmatch(sick_first_half, event['summary'])

            sick_second_half = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)][ ]' \
                               '[(][S][e][c][o][n][d][ ][H][a][l][f][-][D][a][y][)]'
            condition_sick_second_half = re.fullmatch(sick_second_half, event['summary'])

            sick_first_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)][ ]' \
                                 '[(][F][i][r][s][t][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_sick_first_quarter = re.fullmatch(sick_first_quarter, event['summary'])

            sick_second_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)]' \
                                  '[ ][(][S][e][c][o][n][d][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_sick_second_quarter = re.fullmatch(sick_second_quarter, event['summary'])

            sick_third_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)]' \
                                 '[ ][(][T][h][i][r][d][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_sick_third_quarter = re.fullmatch(sick_third_quarter, event['summary'])

            sick_fourth_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[S][i][c][k][ ][L][e][a][v][e][ ][(][I][n][d][i][a][)]' \
                                  '[ ][(][F][o][u][r][t][h][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_sick_fourth_quarter = re.fullmatch(sick_fourth_quarter, event['summary'])

            # Earned Leave
            earned_leave_full_day = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ]' \
                                    '[(][I][n][d][i][a][)]'
            condition_earned_leave_full_day = re.fullmatch(earned_leave_full_day, event['summary'])

            earned_leave_first_half = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ]' \
                                      '[(][I][n][d][i][a][)][ ][(][F][i][r][s][t][ ][H][a][l][f][-][D][a][y][)]'
            condition_earned_leave_first_half = re.fullmatch(earned_leave_first_half, event['summary'])

            earned_leave_second_half = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ]' \
                                       '[(][I][n][d][i][a][)][ ][(][S][e][c][o][n][d][ ][H][a][l][f][-][D][a][y][)]'
            condition_earned_leave_second_half = re.fullmatch(earned_leave_second_half, event['summary'])

            earned_leave_first_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ][(][I][n]' \
                                         '[d][i][a][)][ ][(][F][i][r][s][t][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_earned_leave_first_quarter = re.fullmatch(earned_leave_first_quarter, event['summary'])

            earned_leave_second_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ][(][I][n]' \
                                          '[d][i][a][)][ ][(][S][e][c][o][n][d][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_earned_leave_second_quarter = re.fullmatch(earned_leave_second_quarter, event['summary'])

            earned_leave_third_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ][(][I][n]' \
                                         '[d][i][a][)][ ][(][T][h][i][r][d][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_earned_leave_third_quarter = re.fullmatch(earned_leave_third_quarter, event['summary'])

            earned_leave_fourth_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[E][a][r][n][e][d][ ][L][e][a][v][e][ ][(][I][n]' \
                                          '[d][i][a][)][ ][(][F][o][u][r][t][h][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_earned_leave_fourth_quarter = re.fullmatch(earned_leave_fourth_quarter, event['summary'])

            # Compensatory Off
            compensatory_leave_full_day = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ][O][f][f]' \
                                          '[ ][(][I][n][d][i][a][)]'
            condition_compensatory_leave_full_day = re.fullmatch(compensatory_leave_full_day, event['summary'])

            compensatory_leave_first_half = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ][O][f]' \
                                            '[f][ ][(][I][n][d][i][a][)][ ][(][F][i][r][s][t][ ][H][a][l][f][-]' \
                                            '[D][a][y][)]'
            condition_compensatory_leave_first_half = re.fullmatch(compensatory_leave_first_half, event['summary'])

            compensatory_leave_second_half = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ][O][f]' \
                                             '[f][ ][(][I][n][d][i][a][)][ ][(][S][e][c][o][n][d][ ][H][a][l][f][-]' \
                                             '[D][a][y][)]'
            condition_compensatory_leave_second_half = re.fullmatch(compensatory_leave_second_half, event['summary'])

            compensatory_leave_first_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ][O]' \
                                               '[f][f][ ][(][I][n][d][i][a][)][ ][(][F][i][r][s][t][ ][Q][u][a][r][t]' \
                                               '[e][r][-][D][a][y][)]'
            condition_compensatory_leave_first_quarter = re.fullmatch(compensatory_leave_first_quarter,
                                                                      event['summary'])

            compensatory_leave_second_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ]' \
                                                '[O][f][f][ ][(][I][n][d][i][a][)][ ][(][S][e][c][o][n][d][ ][Q][u]' \
                                                '[a][r][t][e][r][-][D][a][y][)]'
            condition_compensatory_leave_second_quarter = re.fullmatch(compensatory_leave_second_quarter,
                                                                       event['summary'])
            compensatory_leave_third_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ]' \
                                               '[O][f][f][ ][(][I][n][d][i][a][)][ ][(][T][h][i][r][d][ ][Q][u][a][r]' \
                                               '[t][e][r][-][D][a][y][)]'
            condition_compensatory_leave_third_quarter = re.fullmatch(compensatory_leave_third_quarter,
                                                                      event['summary'])
            compensatory_leave_fourth_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[C][o][m][p][e][n][s][a][t][o][r][y][ ]' \
                                                '[O][f][f][ ][(][I][n][d][i][a][)][ ][(][F][o][u][r][t][h][ ][Q][u]' \
                                                '[a][r][t][e][r][-][D][a][y][)]'
            condition_compensatory_leave_fourth_quarter = re.fullmatch(compensatory_leave_fourth_quarter,
                                                                       event['summary'])

            # Work From Home
            work_from_home = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ][(][2][ ][d][a]' \
                             '[y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)]'
            condition_work_from_home = re.fullmatch(work_from_home, event['summary'])

            work_from_home_first_half = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ][(]' \
                                        '[2][ ][d][a][y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)][ ][(][F][i][r]' \
                                        '[s][t][ ][H][a][l][f][-][D][a][y][)]'
            condition_wfh_first_half = re.fullmatch(work_from_home_first_half, event['summary'])

            work_from_home_second_half = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ][(]' \
                                         '[2][ ][d][a][y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)][ ][(][S][e][c]' \
                                         '[o][n][d][ ][H][a][l][f][-][D][a][y][)]'
            condition_wfh_second_half = re.fullmatch(work_from_home_second_half, event['summary'])

            work_from_home_first_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ]' \
                                           '[(][2][ ][d][a][y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)][ ][(][F]' \
                                           '[i][r][s][t][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_wfh_first_quarter = re.fullmatch(work_from_home_first_quarter, event['summary'])

            work_from_home_second_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ]' \
                                            '[(][2][ ][d][a][y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)][ ][(][S]' \
                                            '[e][c][o][n][d][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_wfh_second_quarter = re.fullmatch(work_from_home_second_quarter, event['summary'])

            work_from_home_third_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ]' \
                                           '[(][2][ ][d][a][y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)][ ][(][T]' \
                                           '[h][i][r][d][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_wfh_third_quarter = re.fullmatch(work_from_home_third_quarter, event['summary'])

            work_from_home_fourth_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[W][o][r][k][ ][f][r][o][m][ ][h][o][m][e][ ]' \
                                            '[(][2][ ][d][a][y][s][ ][a][d][v][a][n][c][e][ ][o][n][l][y][)][ ][(]' \
                                            '[F][o][u][r][t][h][ ][Q][u][a][r][t][e][r][-][D][a][y][)]'
            condition_wfh_fourth_quarter = re.fullmatch(work_from_home_fourth_quarter, event['summary'])

            # FOP
            fop_leave_full_day = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e][m]' \
                                 '[p][l][o][y][e][e][s][ ][o][n][l][y][)]'
            condition_fop_full_day = re.fullmatch(fop_leave_full_day, event['summary'])

            fop_leave_first_half = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e][m]' \
                                   '[p][l][o][y][e][e][s][ ][o][n][l][y][)][ ][(][F][i][r][s][t][ ][H][a][l][f][-]' \
                                   '[D][a][y][)]'
            condition_fop_first_half = re.fullmatch(fop_leave_first_half, event['summary'])

            fop_leave_second_half = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e][m]' \
                                    '[p][l][o][y][e][e][s][ ][o][n][l][y][)][ ][(][S][e][c][o][n][d][ ][H][a][l][f]' \
                                    '[-][D][a][y][)]'
            condition_fop_second_half = re.fullmatch(fop_leave_second_half, event['summary'])

            fop_leave_first_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e]' \
                                      '[m][p][l][o][y][e][e][s][ ][o][n][l][y][)][ ][(][F][i][r][s][t][ ][Q][u][a][r]' \
                                      '[t][e][r][-][D][a][y][)]'
            condition_fop_first_quarter = re.fullmatch(fop_leave_first_quarter, event['summary'])

            fop_leave_second_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e]' \
                                       '[m][p][l][o][y][e][e][s][ ][o][n][l][y][)][ ][(][S][e][c][o][n][d][ ][Q][u]' \
                                       '[a][r][t][e][r][-][D][a][y][)]'
            condition_fop_second_quarter = re.fullmatch(fop_leave_second_quarter, event['summary'])

            fop_leave_third_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e]' \
                                      '[m][p][l][o][y][e][e][s][ ][o][n][l][y][)][ ][(][T][h][i][r][d][ ][Q][u][a][r]' \
                                      '[t][e][r][-][D][a][y][)]'
            condition_fop_third_quarter = re.fullmatch(fop_leave_third_quarter, event['summary'])

            fop_leave_fourth_quarter = '[H][R][M]+[0-9]+[ ][-][ ]+[F][O][P][ ][(][F][o][r][ ][f][e][m][a][l][e][ ][e]' \
                                       '[m][p][l][o][y][e][e][s][ ][o][n][l][y][)][ ][(][F][o][u][r][t][h][ ][Q][u]' \
                                       '[a][r][t][e][r][-][D][a][y][)]'
            condition_fop_fourth_quarter = re.fullmatch(fop_leave_fourth_quarter, event['summary'])

            # Restricted Holiday
            restricted_holiday = '[H][R][M]+[0-9]+[ ][-][ ]+[R][e][s][t][r][i][c][t][e][d][ ][H][o][l][i][d][a][y]'
            condition_restricted_holiday = re.fullmatch(restricted_holiday, event['summary'])

            if condition_sick_all_day is not None:
                if event['start'].get('dateTime'):
                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (SICK LEAVE - Hours Based)',
                            "description": 'Sick Leave Hours Based',
                            "colorId": '11',
                            "start": {"dateTime": event['start'].get('dateTime'), "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": event['end'].get('dateTime'), "timeZone": 'Asia/Kolkata'}
                        },
                    ).execute()

                    print("*** Hours Based Sick Leave Event Updated Successfully ***")

                else:
                    event_original_date = event['start'].get('date')
                    date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                    event_date = datetime.datetime(date.year, date.month, date.day, 9)
                    start = event_date.isoformat()
                    end = (event_date + timedelta(hours=9)).isoformat()

                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (SICK LEAVE - Full Day)',
                            "description": 'Full Day Sick Leave - 9AM to 6PM',
                            "colorId": '11',
                            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                        },
                    ).execute()

                    print("*** All Day Sick Leave Event Updated Successfully ***")

            # First Half Sick Leave (9-AM to 1-PM)

            elif condition_sick_first_half is not None:
                event_original_date = event['start'].get('date')
                # date_format = datetime.datetime.fromisoformat(event_original_date).astimezone(timezone.utc)
                # date_str = date_format.strftime('%Y-%m-%d')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (SICK LEAVE - First Half)',
                        "description": 'First Half Sick Leave - 9AM to 1PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** First Half Sick Event Updated Successfully ***")

            # Second Half Sick Leave (1-PM to 6-PM)

            elif condition_sick_second_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (SICK LEAVE - Second Half)',
                        "description": 'Second Half Sick Leave - 1PM to 6PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Second Half Sick Event Updated Successfully ***")

            # First Quarter Sick Leave (9-AM to 11-AM)

            elif condition_sick_first_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (SICK LEAVE - First Quarter)',
                        "description": 'First Quarter Sick Leave - 9AM to 11AM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** First Quarter Sick Event Updated Successfully ***")

            # Second Quarter Sick Leave (11-AM to 1-PM)

            elif condition_sick_second_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 11)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (SICK LEAVE - Second Quarter)',
                        "description": 'Second Quarter Sick Leave - 11AM to 1PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Second Quarter Sick Event Updated Successfully ***")

            # Third Quarter Sick Leave (2-PM to 4-PM)

            elif condition_sick_third_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (SICK LEAVE - Third Quarter)',
                        "description": 'Third Quarter Sick Leave - 2PM to 4PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Third Quarter Sick Event Updated Successfully ***")

            # Fourth Quarter Sick Leave (4-PM to 6-PM)

            elif condition_sick_fourth_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 16)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (SICK LEAVE - Forth Quarter)',
                        "description": 'Fourth Quarter Sick Leave - 4PM to 6PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Fourth Quarter Sick Event Updated Successfully ***")

            # Earned Leave Full Day (9-AM to 6-PM)

            elif condition_earned_leave_full_day is not None:
                if event['start'].get('dateTime'):
                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (Earned Leave - Hours Based)',
                            "description": 'Sick Leave Hours Based',
                            "colorId": '11',
                            "start": {"dateTime": event['start'].get('dateTime'), "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": event['end'].get('dateTime'), "timeZone": 'Asia/Kolkata'}
                        },
                    ).execute()

                    print("*** Hours Based Earned Event Updated Successfully ***")

                else:
                    event_original_date = event['start'].get('date')
                    date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                    event_date = datetime.datetime(date.year, date.month, date.day, 9)
                    start = event_date.isoformat()
                    end = (event_date + timedelta(hours=9)).isoformat()

                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (EARNED LEAVE - Full Day)',
                            "description": 'Full Day Earned Leave - 9AM to 6PM',
                            "colorId": '11',
                            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                        },
                    ).execute()

                    print("*** Earned Leave Full Day Event Updated Successfully ***")

            # Earned Leave First Half Day (9-AM to 1-PM)

            elif condition_earned_leave_first_half:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (EARNED LEAVE - First Half)',
                        "description": 'First Half Earned Leave - 9AM to 1AM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Earned Leave First Half Event Updated Successfully ***")

            # Earned Leave Second Half Day (2-PM to 6-PM)

            elif condition_earned_leave_second_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (EARNED LEAVE - Second Half)',
                        "description": 'Second Half Earned Leave - 1PM to 6PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Earned Leave Second Half Event Updated Successfully ***")

            # Earned Leave First Quarter (9-AM to 11-AM)

            elif condition_earned_leave_first_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (EARNED LEAVE - First Quarter)',
                        "description": 'First Quarter Earned Leave - 9AM to 11AM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Earned Leave First Quarter Event Updated Successfully ***")

            # Earned Leave Second Quarter (11-AM to 1-PM)

            elif condition_earned_leave_second_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 11)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (EARNED LEAVE - Second Quarter)',
                        "description": 'Second Quarter Earned Leave - 11AM to 1PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Earned Leave Second Quarter Event Updated Successfully ***")

            # Earned Leave Third Quarter (2-PM to 4-PM)

            elif condition_earned_leave_third_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (EARNED LEAVE - Third Quarter)',
                        "description": 'Third Quarter Earned Leave - 1PM to 4PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Earned Leave Third Quarter Event Updated Successfully ***")

            # Earned Leave Fourth Quarter (4-PM to 6-PM)

            elif condition_earned_leave_fourth_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 16)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (EARNED LEAVE - Fourth Quarter)',
                        "description": 'Fourth Quarter Earned Leave - 4PM to 6PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Earned Leave Fourth Quarter Event Updated Successfully ***")

            # Compensatory Off Full Day (9-AM to 6-PM)

            elif condition_compensatory_leave_full_day is not None:
                if event['start'].get('dateTime'):
                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (COMPENSATORY OFF - Hours Based)',
                            "description": 'Compensatory Off Hours Based',
                            "colorId": '11',
                            "start": {"dateTime": event['start'].get('dateTime'), "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": event['end'].get('dateTime'), "timeZone": 'Asia/Kolkata'}
                        },
                    ).execute()

                    print("*** Hours Based Compensatory Event Updated Successfully ***")

                else:
                    event_original_date = event['start'].get('date')
                    date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                    event_date = datetime.datetime(date.year, date.month, date.day, 9)
                    start = event_date.isoformat()
                    end = (event_date + timedelta(hours=9)).isoformat()

                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (COMPENSATORY OFF - Full Day)',
                            "description": 'Full Day Compensatory Leave - 9AM to 6PM',
                            "colorId": '11',
                            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                        },
                    ).execute()

                    print("*** Compensatory Off Event Updated Successfully ***")

            # First Half Compensatory Off (9-AM to 1-PM)

            elif condition_compensatory_leave_first_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (COMPENSATORY OFF - First Half)',
                        "description": 'First Half Compensatory Leave - 9AM to 1PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # Second Half Compensatory Off (1-PM to 6-PM)

            elif condition_compensatory_leave_second_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (COMPENSATORY OFF - Second Half)',
                        "description": 'Second Half Compensatory Leave - 1PM to 6PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # First Quarter Compensatory Off (9-AM to 11-AM)

            elif condition_compensatory_leave_first_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (COMPENSATORY OFF - First Quarter)',
                        "description": 'First Quarter Compensatory Leave - 9AM to 11AM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # Second Quarter Compensatory Off (11-AM to 1-PM)

            elif condition_compensatory_leave_second_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 11)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (COMPENSATORY OFF - Second Quarter)',
                        "description": 'Second Quarter Compensatory Leave - 11AM to 1PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # Third Quarter Compensatory Off (2-PM to 4-PM)

            elif condition_compensatory_leave_third_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (COMPENSATORY OFF - Third Quarter)',
                        "description": 'Third Quarter Compensatory Leave - 2PM to 4PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # Fourth Quarter Compensatory Off (4-PM to 6-PM)

            elif condition_compensatory_leave_fourth_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 16)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (COMPENSATORY OFF - Forth Quarter)',
                        "description": 'Fourth Quarter Compensatory Leave - 4PM to 6PM',
                        "colorId": '11',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # Work From Home (9-AM to 6-PM)

            elif condition_work_from_home is not None:
                if event['start'].get('dateTime'):
                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (WORK FROM HOME - Full Day)',
                            "description": 'WORK FROM HOME',
                            "colorId": '2',
                            "start": {"dateTime": event['start'].get('dateTime'), "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": event['end'].get('dateTime'), "timeZone": 'Asia/Kolkata'}
                        },
                    ).execute()

                    print("*** Work From Home Event Updated Successfully ***")

                else:
                    event_original_date = event['start'].get('date')
                    date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                    event_date = datetime.datetime(date.year, date.month, date.day, 9)
                    start = event_date.isoformat()
                    end = (event_date + timedelta(hours=9)).isoformat()

                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (WORK FROM HOME - Full Day)',
                            "description": 'Work From Home - 9AM to 6PM',
                            "colorId": '2',  # 4, 10, 2
                            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                        },
                    ).execute()

                    print("*** Work From Home Event Updated Successfully ***")

            # First Half Work From Home (9-AM to 1-PM)

            elif condition_wfh_first_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (WORK FROM HOME - First Half)',
                        "description": 'First Half Compensatory Leave - 9AM to 1PM',
                        "colorId": '2',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Work From Home Event Updated Successfully ***")

            # Second Half Work From Home (1-PM to 6-PM)

            elif condition_wfh_second_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (WORK FROM HOME - Second Half)',
                        "description": 'Second Half Work From Home - 1PM to 6PM',
                        "colorId": '2',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Compensatory Off Event Updated Successfully ***")

            # First Quarter WFH (9-AM to 11-AM)

            elif condition_wfh_first_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (WORK FROM HOME - First Quarter)',
                        "description": 'First Quarter Work From Home - 9AM to 11AM',
                        "colorId": '2',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Work From Home Event Updated Successfully ***")

            # Second Quarter WFH (11-AM to 1-PM)

            elif condition_wfh_second_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 11)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (WORK FROM HOME - Second Quarter)',
                        "description": 'Second Quarter Work From Home - 11AM to 1PM',
                        "colorId": '2',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Work From Home Event Updated Successfully ***")

            # Third Quarter WFH (2-PM to 4-PM)

            elif condition_wfh_third_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (WORK FROM HOME - Third Quarter)',
                        "description": 'Third Quarter Work From Home - 2PM to 4PM',
                        "colorId": '2',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Work From Home Event Updated Successfully ***")

            # Fourth Quarter WFH (4-PM to 6-PM)

            elif condition_wfh_fourth_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 16)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (WORK FROM HOME - Forth Quarter)',
                        "description": 'Fourth Quarter Work from home - 4PM to 6PM',
                        "colorId": '2',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** Work From Home Event Updated Successfully ***")

            # FOP (9-AM to 6-PM)

            elif condition_fop_full_day is not None:
                if event['start'].get('dateTime'):
                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (FOP - Full Day)',
                            "description": 'FOP (For Female Employees Only) (Full Day) - 9-AM to 6-PM',
                            "colorId": '3',
                            "start": {"dateTime": event['start'].get('dateTime'), "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": event['end'].get('dateTime'), "timeZone": 'Asia/Kolkata'}
                        },
                    ).execute()

                    print("*** FOP Event Updated Successfully ***")

                else:
                    event_original_date = event['start'].get('date')
                    date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                    event_date = datetime.datetime(date.year, date.month, date.day, 9)
                    start = event_date.isoformat()
                    end = (event_date + timedelta(hours=9)).isoformat()

                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (FOP - Full Day)',
                            "description": 'FOP (For Female Employees Only) (Full Day) - 9AM to 6PM',
                            "colorId": '3',
                            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                        },
                    ).execute()

                    print("*** FOP Event Updated Successfully ***")

            # First Half FOP (9-AM to 1-PM)

            elif condition_fop_first_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (FOP - First Half)',
                        "description": 'FOP (For Female Employees Only) (First Half) - 9AM to 1PM',
                        "colorId": '3',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** FOP Event Updated Successfully ***")

            # Second Half FOP (1-PM to 6-PM)

            elif condition_fop_second_half is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=4)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (FOP - Second Half)',
                        "description": 'FOP (For Female Employees Only) (Second Half) - 1PM to 6PM',
                        "colorId": '3',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** FOP Event Updated Successfully ***")

            # First Quarter FOP Off (9-AM to 11-AM)

            elif condition_fop_first_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 9)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (FOP - First Quarter)',
                        "description": 'FOP (For Female Employees Only) (First Quarter) - 9AM to 11AM',
                        "colorId": '3',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** FOP Event Updated Successfully ***")

            # Second Quarter Compensatory Off (11-AM to 1-PM)

            elif condition_fop_second_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 11)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (FOP - Second Quarter)',
                        "description": 'FOP (For Female Employees Only) (Second Quarter) - 11AM to 1PM',
                        "colorId": '3',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** FOP Event Updated Successfully ***")

            # Third Quarter FOP Off (2-PM to 4-PM)

            elif condition_fop_third_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 14)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (FOP - Third Quarter)',
                        "description": 'FOP (For Female Employees Only) (Third Quarter) - 2PM to 4PM',
                        "colorId": '3',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** FOP Event Updated Successfully ***")

            # Fourth Quarter FOP Off (4-PM to 6-PM)

            elif condition_fop_fourth_quarter is not None:
                event_original_date = event['start'].get('date')
                date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                event_date = datetime.datetime(date.year, date.month, date.day, 16)
                start = event_date.isoformat()
                end = (event_date + timedelta(hours=2)).isoformat()

                event_result = service.events().update(
                    calendarId=cid,
                    eventId=event_id,
                    body={
                        "summary": 'Out of office (FOP - Fourth Quarter)',
                        "description": 'FOP (For Female Employees Only) (Fourth Quarter) - 4PM to 6PM',
                        "colorId": '3',
                        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                    },
                ).execute()

                print("*** FOP Event Updated Successfully ***")

            # Restricted Holiday (9-AM to 6-PM)

            elif condition_restricted_holiday is not None:
                if event['start'].get('dateTime'):
                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (RESTRICTED HOLIDAY)',
                            "description": 'Restricted Holiday - 9AM to 6PM',
                            "colorId": '2',
                            "start": {"dateTime": event['start'].get('dateTime'), "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": event['end'].get('dateTime'), "timeZone": 'Asia/Kolkata'}
                        },
                    ).execute()

                    print("*** RESTRICTED HOLIDAY Event Updated Successfully ***")

                else:
                    event_original_date = event['start'].get('date')
                    date = datetime.datetime.strptime(event_original_date, '%Y-%m-%d').date()
                    event_date = datetime.datetime(date.year, date.month, date.day, 9)
                    start = event_date.isoformat()
                    end = (event_date + timedelta(hours=9)).isoformat()

                    event_result = service.events().update(
                        calendarId=cid,
                        eventId=event_id,
                        body={
                            "summary": 'Out of office (RESTRICTED HOLIDAY)',
                            "description": 'Restricted Holiday - 9AM to 6PM',
                            "colorId": '4',
                            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                        },
                    ).execute()

                    print("*** Restricted Holiday Event Updated Successfully ***")


if __name__ == '__main__':
    main()

schedule.every(1).minute.do(main)
while True:
    schedule.run_pending()
