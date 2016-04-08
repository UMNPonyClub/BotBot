class Problem:
    def __init__(self, code, message, fix):
        self.code = code
        self.message = message
        self.fix = fix

PROB_NO_PROBLEM       = Problem(0, 'Good.', 'Nothing to be done.')
PROB_DIR_NOT_WRITABLE = Problem(1, 'Directory not writable.', 'Run \'chmod 0655\' on this directory.')
PROB_FILE_NOT_GRPRD   = Problem(2, 'File not group readable.', 'Run \'chmod 0644\' on this file.')