from django.core.exceptions import ValidationError


#-- head
class EmptyCoordinates(ValidationError): pass


#-- sale and rent terms
class EmptySalePrice(ValidationError): pass
class EmptyRentPrice(ValidationError): pass


#-- body
class EmptyTitle(ValidationError): pass
class EmptyDescription(ValidationError): pass


#-- validation
class EmptyFloor(ValidationError): pass
class EmptyTotalArea(ValidationError): pass
class EmptyLivingArea(ValidationError): pass
class EmptyHallsArea(ValidationError): pass
class EmptyPlotArea(ValidationError): pass
class EmptyCabinetsArea(ValidationError): pass

class EmptyRoomsCount(ValidationError): pass
class EmptyFloorsCount(ValidationError): pass
class EmptyPersonsCount(ValidationError): pass
class EmptyCabinetsCount(ValidationError): pass
class EmptyHallsCount(ValidationError): pass