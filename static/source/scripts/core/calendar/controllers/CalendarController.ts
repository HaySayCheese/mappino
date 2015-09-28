namespace Mappino.Core.Calendar {

    import IParseService = angular.IParseService;
    import INgModelController = angular.INgModelController;
    import ILogService = angular.ILogService;
    import IFilterService = angular.IFilterService;


    export class CalendarController {

        private currentCalendarDate: Date = new Date();
        private ngModelCtrl: INgModelController;
        private mode: any = {
            step: {
                months: 1
            }
        };

        private formatDay:           string  = 'dd';
        private formatDayHeader:     string  = 'ddd';
        private formatDayTitle:      string  = 'MMMM dd, yyyy';
        //public formatWeekTitle:     string  = 'MMMM yyyy, Week w';
        private formatMonthTitle:    string  = 'MMMM YYYY';
        //public calendarMode:        string  = 'month';
        private showWeeks:           boolean = false;
        private showEventDetail:     boolean = true;
        private startingDay:         any     = '1';
        //public queryMode:           string  = 'local';


        public static $inject = [
            '$scope',
            '$attrs',
            '$parse',
            '$log',
            '$filter'
        ];

        constructor(private $scope: any,
                    private $attrs: any,
                    private $parse: IParseService,
                    private $log: ILogService,
                    private $filter: IFilterService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.range = {
                startTime: undefined,
                endTime: undefined
            };

            $scope.$watchCollection('eventSource', (value) => {
                this.onEventSourceChanged(value);
            });

            if (!this.$scope.currentCalendarDate) {
                this.$scope.currentCalendarDate = new Date();
            }

            this.refreshView();
        }



        public init(ngModelCtrl_) {
            this.ngModelCtrl = ngModelCtrl_;

            this.ngModelCtrl.$render = () => {
                this.render();
            };
        }



        public select(selectedDate) {
            var rows = this.$scope.rows;
            if (rows) {
                var currentCalendarDate = this.$scope.currentCalendarDate;
                var currentMonth = currentCalendarDate.getMonth();
                var currentYear = currentCalendarDate.getFullYear();
                var selectedMonth = selectedDate.getMonth();
                var selectedYear = selectedDate.getFullYear();
                var direction = 0;

                if (currentYear === selectedYear) {
                    if (currentMonth !== selectedMonth) {
                        direction = currentMonth < selectedMonth ? 1 : -1;
                    }
                } else {
                    direction = currentYear < selectedYear ? 1 : -1;
                }

                this.$scope.currentCalendarDate = selectedDate;

                if (direction === 0) {
                    for (var row = 0; row < 6; row += 1) {
                        for (var date = 0; date < 7; date += 1) {
                            var selected = this.compare(selectedDate, rows[row][date].date) === 0;
                            rows[row][date].selected = selected;
                            if (selected) {
                                this.$scope.selectedDate = rows[row][date];
                            }
                        }
                    }
                } else {
                    this.refreshView();
                }

                if (this.$scope.timeSelected) {
                    this.$scope.timeSelected({selectedTime: selectedDate});
                }
            }
        }



        private split(arr, size) {
            var arrays = [];
            while (arr.length > 0) {
                arrays.push(arr.splice(0, size));
            }
            return arrays;
        }



        private render() {
            if (this.ngModelCtrl.$modelValue) {
                var date    = new Date(this.ngModelCtrl.$modelValue),
                    isValid = angular.isDate(date);

                if (isValid) {
                    this.$scope.currentCalendarDate = date;
                } else {
                    this.$log.error('"ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.');
                }

                this.ngModelCtrl.$setValidity('date', isValid);
            }

            this.refreshView();
        }



        private refreshView() {
            this.$scope.range = this.getRange(this.$scope.currentCalendarDate);
            this.refreshMonthView();
            this.rangeChanged();
        }



        private onEventSourceChanged(value) {
            this.$scope.eventSource = value;
            if (this.onDataLoaded) {
                this.onDataLoaded();
            }
        }



        public refreshMonthView() {
            var startDate = this.$scope.range.startTime,
                date = startDate.getDate(),
                month = (startDate.getMonth() + (date !== 1 ? 1 : 0)) % 12,
                year = startDate.getFullYear() + (date !== 1 && month === 0 ? 1 : 0);

            var days = this.getDates(startDate, 42);
            for (var i = 0; i < 42; i++) {
                days[i] = angular.extend(this.createDateObject(days[i], this.formatDay), {
                    secondary: days[i].getMonth() !== month
                });
            }

            this.$scope.labels = new Array(7);
            for (var j = 0; j < 7; j++) {
                this.$scope.labels[j] = moment(days[j].date).format(this.formatDayHeader);
            }

            var headerDate: Date = new Date(year, month, 1);
            this.$scope.title = moment(headerDate).format(this.formatMonthTitle);

            this.$scope.rows = this.split(days, 7);


            if (this.$scope.showWeeks) {
                this.$scope.weekNumbers = [];
                var weekNumber = this.getISO8601WeekNumber(this.$scope.rows[0][0].date),
                    numWeeks = this.$scope.rows.length,
                    len = 0;
                while (len < numWeeks) {
                    len = this.$scope.weekNumbers.push(weekNumber);
                    weekNumber += 1;
                }
            }
        }



        public getRange(currentDate) {
            var year = currentDate.getFullYear(),
                month = currentDate.getMonth(),
                firstDayOfMonth = new Date(year, month, 1),
                difference = this.startingDay - firstDayOfMonth.getDay(),
                numDisplayedFromPreviousMonth = (difference > 0) ? 7 - difference : -difference,
                startDate = new Date(firstDayOfMonth.toString()),
                endDate;

            if (numDisplayedFromPreviousMonth > 0) {
                startDate.setDate(-numDisplayedFromPreviousMonth + 1);
            }

            endDate = new Date(startDate.toString());
            endDate.setDate(endDate.getDate() + 42);

            return {
                startTime: startDate,
                endTime: endDate
            };
        }



        public move(direction) {
            var step = this.mode.step,
                currentCalendarDate = this.$scope.currentCalendarDate,
                year    = currentCalendarDate.getFullYear() + direction * (step.years || 0),
                month   = currentCalendarDate.getMonth() + direction * (step.months || 0),
                date    = currentCalendarDate.getDate() + direction * (step.days || 0),
                firstDayInNextMonth;

            currentCalendarDate.setFullYear(year, month, date);

            firstDayInNextMonth = new Date(year, month + 1, 1);

            if (firstDayInNextMonth.getTime() <= currentCalendarDate.getTime()) {
                this.$scope.currentCalendarDate = new Date(firstDayInNextMonth - 24 * 60 * 60 * 1000);
            }

            this.refreshView();
        }



        public rangeChanged() {
            if (this.$scope.eventSource && this.onDataLoaded) {
                this.onDataLoaded();
            }
        }



        public onDataLoaded() {
            var eventSource = this.$scope.eventSource,
                len = eventSource ? eventSource.length : 0,
                startTime = this.$scope.range.startTime,
                endTime = this.$scope.range.endTime,
                rows = this.$scope.rows,
                oneDay = 86400000,
                eps = 0.001,
                row,
                date,
                hasEvent = false;

            if (rows.hasEvent) {
                for (row = 0; row < 6; row += 1) {
                    for (date = 0; date < 7; date += 1) {
                        if (rows[row][date].hasEvent) {
                            rows[row][date].events = null;
                            rows[row][date].hasEvent = false;
                        }
                    }
                }
            }

            for (var i = 0; i < len; i += 1) {
                var event = eventSource[i];
                var eventStartTime: any = new Date(event.startTime);
                var eventEndTime: any = new Date(event.endTime);
                var st;
                var et;
                if (eventEndTime <= startTime || eventStartTime >= endTime) {
                    continue;
                } else {
                    st = startTime;
                    et = endTime;
                }

                var timeDifferenceStart: any;
                if (eventStartTime <= st) {
                    timeDifferenceStart = 0;
                } else {
                    timeDifferenceStart = (eventStartTime - st) / oneDay;
                }

                var timeDifferenceEnd: any;
                if (eventEndTime >= et) {
                    timeDifferenceEnd = (et - st) / oneDay;
                } else {
                    timeDifferenceEnd = (eventEndTime - st) / oneDay;
                }

                var index = Math.floor(timeDifferenceStart);
                var eventSet;
                while (index < timeDifferenceEnd - eps) {
                    var rowIndex = Math.floor(index / 7);
                    var dayIndex = Math.floor(index % 7);
                    rows[rowIndex][dayIndex].hasEvent = true;
                    eventSet = rows[rowIndex][dayIndex].events;
                    if (eventSet) {
                        eventSet.push(event);
                    } else {
                        eventSet = [];
                        eventSet.push(event);
                        rows[rowIndex][dayIndex].events = eventSet;
                    }
                    index += 1;
                }
            }

            for (row = 0; row < 6; row += 1) {
                for (date = 0; date < 7; date += 1) {
                    if (rows[row][date].hasEvent) {
                        hasEvent = true;
                        //rows[row][date].events.sort(compareEvent);
                    }
                }
            }
            rows.hasEvent = hasEvent;

            var findSelected = false;
            for (row = 0; row < 6; row += 1) {
                for (date = 0; date < 7; date += 1) {
                    if (rows[row][date].selected) {
                        this.$scope.selectedDate = rows[row][date];
                        findSelected = true;
                        break;
                    }
                }
                if (findSelected) {
                    break;
                }
            }
        }



        private getDates(startDate, n) {
            var dates   = new Array(n),
                current = new Date(startDate),
                i = 0;

            current.setHours(12); // Prevent repeated dates because of timezone bug

            while (i < n) {
                dates[i++] = new Date(current.toString());
                current.setDate(current.getDate() + 1);
            }
            return dates;
        }



        private createDateObject(date, format) {
            return {
                date: date,
                label: this.$filter('date')(date, format),
                selected: this.compare(date, this.$scope.currentCalendarDate) === 0,
                current: this.compare(date, new Date()) === 0
            };
        }



        private getISO8601WeekNumber(date) {
            var checkDate: any = new Date(date);
            checkDate.setDate(checkDate.getDate() + 4 - (checkDate.getDay() || 7)); // Thursday
            var time = checkDate.getTime();
            checkDate.setMonth(0); // Compare with Jan 1
            checkDate.setDate(1);
            return Math.floor(Math.round((time - checkDate) / 86400000) / 7) + 1;
        }



        private compare(date1: Date, date2: Date) {
            var firstDate: any  = new Date(date1.getFullYear(), date1.getMonth(), date1.getDate());
            var secondDate: any = new Date(date2.getFullYear(), date2.getMonth(), date2.getDate());

            return (firstDate - secondDate);
        };



        private overlap(event1, event2) {
            if (event1.endIndex <= event2.startIndex || event2.endIndex <= event1.startIndex) {
                return false;
            }
            return true;
        }



        private calculatePosition(events) {
            var i,
                j,
                len = events.length,
                maxColumn = 0,
                col,
                isForbidden = new Array(len);

            for (i = 0; i < len; i += 1) {
                for (col = 0; col < maxColumn; col += 1) {
                    isForbidden[col] = false;
                }
                for (j = 0; j < i; j += 1) {
                    if (this.overlap(events[i], events[j])) {
                        isForbidden[events[j].position] = true;
                    }
                }
                for (col = 0; col < maxColumn; col += 1) {
                    if (!isForbidden[col]) {
                        break;
                    }
                }
                if (col < maxColumn) {
                    events[i].position = col;
                } else {
                    events[i].position = maxColumn++;
                }
            }
        }



        private calculateWidth(orderedEvents) {
            var cells = new Array(24),
                event,
                index,
                i,
                j,
                len,
                eventCountInCell,
                currentEventInCell;

            //sort by position in descending order, the right most columns should be calculated first
            orderedEvents.sort((eventA, eventB) => {
                return eventB.position - eventA.position;
            });

            for (i = 0; i < 24; i += 1) {
                cells[i] = {
                    calculated: false,
                    events: []
                };
            }

            for (i = 0, len = orderedEvents.length; i < len; i += 1) {
                event = orderedEvents[i];
                index = event.startIndex;

                while (index < event.endIndex) {
                    cells[index].events.push(event);
                    index += 1;
                }
            }

            i = 0;
            while (i < len) {
                event = orderedEvents[i];
                if (!event.overlapNumber) {
                    var overlapNumber = event.position + 1;
                    event.overlapNumber = overlapNumber;
                    var eventQueue = [event];
                    while ((event = eventQueue.shift())) {
                        index = event.startIndex;
                        while (index < event.endIndex) {
                            if (!cells[index].calculated) {
                                cells[index].calculated = true;
                                if (cells[index].events) {
                                    eventCountInCell = cells[index].events.length;
                                    for (j = 0; j < eventCountInCell; j += 1) {
                                        currentEventInCell = cells[index].events[j];
                                        if (!currentEventInCell.overlapNumber) {
                                            currentEventInCell.overlapNumber = overlapNumber;
                                            eventQueue.push(currentEventInCell);
                                        }
                                    }
                                }
                            }
                            index += 1;
                        }
                    }
                }
                i += 1;
            }
        }



        public placeEvents(orderedEvents) {
            this.calculatePosition(orderedEvents);
            this.calculateWidth(orderedEvents);
        }



        public placeAllDays(orderedEvents) {
            this.calculatePosition(orderedEvents);
        }
    }
}