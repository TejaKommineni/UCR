import unittest
from flask.ext.testing import TestCase
import app
from app.database import db
from datetime import datetime
import app.models as models

"""
    A suite of tests to run when there is blank database
    
    - Get root node
    - Get empty responses
    - Add data
   
    Creates all tables from scratch before each test,
    Dumps all tables at the end of each test
   
"""
class BlankDB(TestCase):
    def create_app(self):
        # pass in test configuration
        return app.create_app('test_config')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestRoot(BlankDB):        
    # Test the root node    
    def test_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.json, {
            "version" : 0.01,
            "endpoints" : [
                "projects",
                "staff"
            ]})       

class TestArcReview(BlankDB):
    def test_empty_arc_review(self):
        response = self.client.get("/api/arcreviews/")
        self.assertEqual(response.json, {"arcReviews" : []})
        
    def test_arc_review_no_id(self):
        response = self.client.get("/api/arcreviews/1/")
        self.assertEqual(response.json, {"Error" : "ArcReviewID 1 not found"})
    
    def test_create_arc_review(self):
        response = self.client.post("/api/arcreviews/", data = {
            "projectID" : 1,
            "review_type" : 1,
            "date_sent_to_reviewer" : "2016-02-02",
            "reviewer1" : 1,
            "reviewer1_rec" : 1,
            "reviewer1_sig_date" : "2016-02-02",
            "reviewer1_comments" : "test comment",
            "reviewer2" : 2,
            "reviewer2_rec"  :2 ,
            "reviewer2_sig_date" : "2016-02-02",
            "reviewer2_comments" : "2016-02-02",
            "research" : 1,
            "lnkage":False,
            "contact" : True,
            "engaged" : True,
            "non_public_data" : True
        })
        self.assertEqual(response.json, {"arcReviewID" : 1})
            
class TestBudget(BlankDB):
    def test_empty_budget(self):
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.json, {"budgets" : [] })
        
    def test_budget_no_id(self):
        response = self.client.get('/api/budgets/1/')
        self.assertEqual(response.json, {"Error" : "BudgetID 1 not found"})
        
    def test_create_budget(self):
        response = self.client.post("/api/budgets/", data = {
            "projectID" : 1,
            "numPeriods" : 2,
            "periodStart" : "2016-02-02",
            "periodEnd" : "2016-02-02",
            "periodTotal" : 1.2,
            "periodComment" : "comment"
        })
        self.assertEqual(response.json, dict(budgetID=1))

class TestFunding(BlankDB):

    def test_empty_funding(self):
        response = self.client.get("/api/fundings/")
        self.assertEqual(response.json, dict(Fundings = []))
   
    def test_funding_no_id(self):
        response = self.client.get("/api/fundings/1/")
        self.assertEqual(response.json, {"Error" : "FundingID 1 not found"})

    def test_create_funding(self):
        response = self.client.post("/api/fundings/", data = {
            "grantStatusLUTID": 1,
            "projectID": 1,
            "fundingSourceLUTID": 1,
            "primary_funding_source" : "fs 1",
            "secondary_funding_source": "fs 2",
            "funding_number": "number",
            "grant_title" : "title",
            "grantStatusID" : 1,
            "date_status" : "2016-02-02",
            "grant_pi": 1,
            "primary_chartfield" : "chartfield 1",
            "secondary_chartfield" : "chartfield 2"
        })
        self.assertEqual(response.json, {"fundingID": 1})
        
class TestFundingSource(BlankDB):

    def test_empty_funding_source(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json, dict(FundingSources = []))
   
    def test_funding_source__no_id(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json, {"Error" : "FundingSourceLUTID 1 not found"})

    def test_create_funding_source(self):
        response = self.client.post("/api/fundingsources/", data = {
            "fundingSource" : "fs",
        })
        self.assertEqual(response.json, {"fundingSourceLUTID": 1})
        
class TestGrantStatus(BlankDB):

    def test_empty_grant_status(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json, dict(GrantStatuses = []))
   
    def test_grant_status__no_id(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json, {"Error" : "GrantStatusLUTID 1 not found"})

    def test_create_grant_status(self):
        response = self.client.post("/api/grantstatuses/", data = {
            "grant_status" : "status",
        })
        self.assertEqual(response.json, {"grantStatusLUTID": 1})
        
class TestIRBHolder(BlankDB):
    def test_empty_irb_holder(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json, {"irbHolders" : []})
    
    def test_irb_holder_no_id(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json, {"Error" : "IrbHolderID 1 not found"})
        
    def test_create_irb_holder(self):
        response = self.client.post("/api/irbholders/", data = {
            "irb_holder" : "test holder",
            "irb_holder_definition" : "test holder def"
            })
        self.assertEqual(response.json, dict(irbHolderID=1))

class TestLog(BlankDB):
    def test_empty_log(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.json, {"Logs" : []})
    
    def test_log_no_id(self):
        response = self.client.get("/api/logs/1/")
        self.assertEqual(response.json, {"Error" : "LogID 1 not found"})
        
    def test_create_log(self):
        response = self.client.post("/api/logs/", data = {
            "logSubjectLUTID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "phaseStatusID" : 1,
            "note" : "note",
            "date" : "2016-02-02"
            })
        self.assertEqual(response.json, dict(logID=1))
        
class TestLogSubject(BlankDB):
    def test_empty_log_subject(self):
        response = self.client.get("/api/logsubjects/")
        self.assertEqual(response.json, {"LogSubjects" : []})
    
    def test_log_subject_no_id(self):
        response = self.client.get("/api/logsubjects/1/")
        self.assertEqual(response.json, {"Error" : "LogSubjectLUTID 1 not found"})
        
    def test_create_log_subject(self):
        response = self.client.post("/api/logsubjects/", data = {
            "log_subject" : "subject",
            })
        self.assertEqual(response.json, dict(logSubjectLUTID=1))
        
class TestPatient(BlankDB):
    def test_empty_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json, dict(Patients = []))
   
    def test_patient_no_id(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json, {"Error" : "PatAutoID 1 not found"})

    def test_create_patient(self):
        response = self.client.post("/api/patients/", data = {
            "patID" : 1,
            "recordID" : 1,
            "ucrDistID" : 1,
            "UPDBID" : 1,
            "fname" : "fname",
            "lname" : "lname",
            "middle_name" : "mname",
            "maiden_name" : "madien_name",
            "alias_fname" : "alias_fname",
            "alias_lname" : "alias_lname",
            "alias_middle_name" : "alias_middle",
            "dob" : "2016-02-02",
            "SSN" : "999999999",
            "sex" : "male",
            "race" : "white",
            "ethnicity" : "hispanic",
            "vital_status" : "v1"
        })
        self.assertEqual(response.json, {"patAutoID": 1})

class TestPhaseStatus(BlankDB):
    def test_empty_phase_status(self):
        response = self.client.get("/api/phasestatuses/")
        self.assertEqual(response.json, dict(PhaseStatuses = []))
   
    def test_phase_status_no_id(self):
        response = self.client.get("/api/phasestatuses/1/")
        self.assertEqual(response.json, {"Error" : "LogPhaseID 1 not found"})

    def test_create_phase_status(self):
        response = self.client.post("/api/phasestatuses/", data = {
            "phase_status" : "status",
            "phase_description" : "description"
        })
        self.assertEqual(response.json, {"logPhaseID": 1})

class TestPreApplication(BlankDB):         
    def test_empty_pre_application(self):
        response = self.client.get("/api/preapplications/")
        self.assertEqual(response.json, dict(PreApplications = []))
   
    def test_pre_application_no_id(self):
        response = self.client.get("/api/preapplications/1/")
        self.assertEqual(response.json, {"Error" : "PreApplicationID 1 not found"})

    def test_create_pre_application(self):
        response = self.client.post("/api/preapplications/", data = {
            "projectID" : 1,
            "pi_fname" : "pi_fname",
            "pi_lname" : "pi_lname",
            "pi_email" : "pi_email",
            "pi_phone" : "pi_phone",
            "contact_fname" : "contact_fname",
            "contact_lname" : "contact_lname",
            "contact_phone" : "contact_phone",
            "contact_email" : "contact_email",
            "institution" : "institution",
            "institution2" : "institution2",
            "uid" : "uid",
            "udoh" : 1,
            "project_title" : "project_title",
            "purpose" : "purpose",
            "irb0" : True,
            "irb1" : True,
            "irb2" : True,
            "irb3" : True,
            "irb4" : True,
            "other_irb" : "other_irb",
            "updb" : True,
            "pt_contact" : True,
            "start_date" : "2016-02-02",
            "link" : True,
            "delivery_date" : "2016-02-02",
            "description" : "description"
        })
        self.assertEqual(response.json, {"preApplicationID": 1})
                
class TestProject(BlankDB):
    # Test for empty array of projects        
    def test_empty_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.json, {
            "projects":[]
            })
    # Test for project not found        
    def test_project_no_id(self):
        response = self.client.get("/api/projects/1/")
        self.assertEqual(response.json, {"Error" : 
            "ProjectID 1 not found"})
    # Test create a project
    # TODO: insert foreign key items first (SQLITE doesn't care) 
    def test_create_project(self):
        response = self.client.post("/api/projects/", data = {
            "projectType_projectTypeID" : 1,
            "IRBHolderLUT_irbHolderID" : 1,
            "project_name" : "Test Project",
            "short_title" : "Test Project",
            "project_summary" : "Summary",
            "sop":"sop",
            "UCR_proposal":"ucr_proposal",
            "budget_doc" : "budget_doc",
            "UCR_fee" : "no",
            "UCR_no_fee" : "yes",
            "budget_end_date" : "2016-02-02",
            "previous_short_title" : "t short",
            "date_added" : "2016-02-02",
            "final_recruitment_report" : "report"})
        self.assertEqual(response.json,dict(projectID=1))

class TestProjectPatient(BlankDB):
    def test_empty_project_patient(self):
        response = self.client.get("/api/projectpatients/")
        self.assertEqual(response.json, dict(ProjectPatients = []))
   
    def test_project_patient_no_id(self):
        response = self.client.get("/api/projectpatients/1/")
        self.assertEqual(response.json, {"Error" : "ParticipantID 1 not found"})

    def test_create_project_patient(self):
        response = self.client.post("/api/projectpatients/", data = {
            "projectID" : 1,
            "staffID" : 1,
            "ctcID" : 1,
            "current_age" : 1,
            "batch"  : 1,
            "sitegrp" : 1,
            "final_code" : 1,
            "final_code_date" : "2016-02-02",
            "enrollment_date" : "2016-02-02",
            "date_coord_signed" : "2016-02-02",
            "import_date" : "2016-02-02",
            "final_code_staff" : 1,
            "enrollment_staff" : 1,
            "date_coord_signed_staff"  : "2016-02-02",
            "abstract_status" : 1,
            "abstract_status_date" : "2016-02-02",
            "abstract_status_staff" : 1,
            "sent_to_abstractor"  : "2016-02-02",
            "sent_to_abstractor_staff" : 1,
            "abstracted_date" : "2016-02-02",
            "abstractor_initials" : "atp",
            "researcher_date" : "2016-02-02",
            "researcher_staff" : 1,
            "consent_link" : "consent",
            "tracing_status" : 1,
            "med_record_release_signed" : True,
            "med_record_release_link" : "link",
            "med_record_release_staff" : 1,
            "med_record_release_date"  : "2016-02-02",
            "survey_to_researcher"  : "2016-02-02",
            "survey_to_researcher_staff" : 1
        })
        self.assertEqual(response.json, {"participantID": 1})

class TestProjectStaff(BlankDB):
    def test_empty_project_staff(self):
        response = self.client.get("/api/projectstaff/")
        self.assertEqual(response.json, {"ProjectStaff" : []})
    
    def test_project_staff_no_id(self):
        response = self.client.get("/api/projectstaff/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStaffID 1 not found"})
        
    def test_create_project_staff(self):
        response = self.client.post("/api/projectstaff/", data = {
            "staffRoleLUTID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "role" : 1,
            "date_pledge" : "2016-02-02",
            "date_revoked" : "2016-02-02",
            "contact" : "yes",
            "inactive" : "no",
            "human_sub_training_exp" : "2016-02-02",
            "human_sub_type_id" : 1,
            "study_role" : 1
            })
        self.assertEqual(response.json, dict(projectStaffID=1))
        
class TestProjectStatus(BlankDB):
    def test_empty_project_status(self):
        response = self.client.get("/api/projectstatuses/")
        self.assertEqual(response.json, dict(ProjectStatuses = []))
   
    def test_project_status_no_id(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStatusID 1 not found"})

    def test_create_project_status(self):
        response = self.client.post("/api/projectstatuses/", data = {
            "projectStatusLUTID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "status_date" : "2016-02-02",
            "status_notes" : "note"
        })
        self.assertEqual(response.json, {"projectStatusID": 1})
        
class TestProjectStatusType(BlankDB):

    def test_empty_project_status_type(self):
        response = self.client.get("/api/projectstatustypes/")
        self.assertEqual(response.json, dict(ProjectStatusTypes = []))
   
    def test_project_status_type_no_id(self):
        response = self.client.get("/api/projectstatustypes/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStatusTypeID 1 not found"})

    def test_create_project_status_type(self):
        response = self.client.post("/api/projectstatustypes/", data = {
            "project_status" : "Status 1",
            "status_definition" : "status def"
        })
        self.assertEqual(response.json, {"projectStatusTypeID": 1})
        
class TestProjectType(BlankDB):

    def test_empty_project_type(self):
        response = self.client.get("/api/projecttypes/")
        self.assertEqual(response.json, dict(ProjectTypes = []))
   
    def test_project_status__no_id(self):
        response = self.client.get("/api/projecttypes/1/")
        self.assertEqual(response.json, {"Error" : "ProjectTypeID 1 not found"})

    def test_create_project_type(self):
        response = self.client.post("/api/projecttypes/", data = {
            "project_type" : 1,
            "project_type_definition" : "type def"
        })
        self.assertEqual(response.json, {"projectTypeID": 1})
 
class TestRCStatusList(BlankDB):
    # Test for empty RCStatusList
    def test_empty_rcStatusList(self):
        response = self.client.get("/api/rcstatuslist/")
        self.assertEqual(response.json, dict(RCStatusList = []))
    # Test for rcStatusList not found    
    def test_rcStatusList_no_id(self):
        response = self.client.get("/api/rcstatuslist/1/")
        self.assertEqual(response.json, {"Error" : "RCStatusID 1 not found"})
    # Test create RCStatusList
    def test_create_rcStatusList(self):
        response = self.client.post("/api/rcstatuslist/", data = {
            "rc_status" : "Status 1",
            "rc_status_definition" : "rc status def"
        })
        self.assertEqual(response.json, {"rcStatusListID": 1})

class TestReviewCommittee(BlankDB):
    def test_empty_review_committee(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json, dict(reviewCommittees = []))
        
    def test_review_committee_no_id(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json, {"Error": "ReviewCommitteeID 1 not found"})
        
    def test_create_review_committee(self):
        response = self.client.post("/api/reviewcommittees/", data = {
            "project_projectID" : 1,
            "RCStatusList_rc_StatusID": 1,
            "reviewCommitteeList_rcListID": 1,
            "review_committee_number":"1",
            "date_initial_review":"2016-02-02",
            "date_expires" : "2016-02-02",
            "rc_note" : "rc_note",
            "rc_protocol" : "rc_proto",
            "rc_approval":"rc_approval"
        })
        self.assertEqual(response.json, {"reviewCommitteeID" : 1})
        
class TestReviewCommitteeList(BlankDB):
    def test_empty_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json, dict(reviewCommitteeList = []))
        
    def test_review_committee_list_no_id(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json, {"Error": "RCListID 1 not found"})
        
    def test_create_review_committee_list(self):
        response = self.client.post("/api/reviewcommitteelist/", data = {
            "reviewCommittee" : "rc test",
            "rc_description" : "rc desc"
            })
        self.assertEqual(response.json, {"rcListID" : 1 })

class TestUCRReport(BlankDB):
    def test_empty_ucr_report(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json, dict(ucrReports = []))
        
    def test_ucr_report_no_id(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json, {"Error": "UcrReportID 1 not found"})
        
    def test_create_ucr_report(self):
        response = self.client.post("/api/ucrreports/", data = {
            "projectID" : 1,
            "report_type" : 1,
            "report_submitted" : "2016-02-02",
            "report_due" : "2016-02-02",
            "report_doc" : "doc"
        })
        self.assertEqual(response.json, {"ucrReportID" : 1})
        
if __name__ == '__main__':
    unittest.main()
    