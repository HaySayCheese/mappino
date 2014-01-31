import logging
from core.sms_dispatcher.limiters import PerDayCountSMSLimiter, PerIPCountSMSLimiter

LIMITERS = {
	'registration_per_number': PerDayCountSMSLimiter(
		prefix = 'sms_lim_reg_number_',
		max_attempts_count = 5,
		log_directive = 'registration: per number limiter - '
	),
    'registration_per_ip': PerIPCountSMSLimiter(
	    prefix = 'sms_lim_rep_ip_',
	    max_attempts_count = 10,
	    log_directive = 'registration: per ip limiter - '
    ),
}

SEND_LOGGER = logging.getLogger('mappino.sms_dispatcher.sender')