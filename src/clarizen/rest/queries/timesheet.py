from enum import Enum

class TimesheetStates( Enum ):
   Unsubmitted = "UnSubmitted"
   PendingApproval = "PendingApproval"
   Approved = "Approved"
   All = "All"
