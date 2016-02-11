import unittest
from flask.ext.testing import TestCase
import app
from app.database import db
from datetime import datetime
import app.models as models

    
###################################################################################################
# Populated database
###################################################################################################
        
class PopulatedDB(TestCase):
    def create_app(self):
        # pass in test configuration
        return app.create_app('test_config')

    def setUp(self):
        db.create_all()
        self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def populate_db(self):
        arcReview = models.ArcReview(
            review_type = 1,
            date_sent_to_reviewer = datetime(2016,2,2),
            reviewer1 = 1,
            reviewer1_rec = 1,
            reviewer1_sig_date = datetime(2016,2,2),
            reviewer1_comments = "test comment",
            reviewer2 = 2,
            reviewer2_rec  =2 ,
            reviewer2_sig_date = datetime(2016,2,2),
            reviewer2_comments = "test comment",
            research = 1,
            lnkage=False,
            contact = True,
            engaged = True,
            non_public_data = True)
            
        budget = models.Budget(
            numPeriods = 1,
            periodStart = datetime(2016,2,2),
            periodEnd = datetime(2016,2,2),
            periodTotal = 1.23,
            periodComment = "comment")
            
        p = models.Project(
            projectType_projectTypeID = 1,
            IRBHolderLUT_irbHolderID = 1,
            project_name = "Test Project",
            short_title = "Test Project",
            project_summary = "Summary",
            sop="sop",
            UCR_proposal="ucr_proposal",
            budget_doc = "budget_doc",
            UCR_fee = "no",
            UCR_no_fee = "yes",
            budget_end_date = datetime(2016,2,2),
            previous_short_title = "t short",
            date_added = datetime(2016,2,2),
            final_recruitment_report = "report")
        rc = models.ReviewCommittee(
            project_projectID=p.projectID,
            RCStatusList_rc_StatusID=1,
            reviewCommitteeList_rcListID=1,
            review_committee_number="1",
            date_initial_review=datetime(2016,2,2),
            date_expires = datetime(2016,2,2),
            rc_note = "rc_note",
            rc_protocol = "rc_proto",
            rc_approval="rc_approval")
            
        ucr = models.UCRReport(
            projectID = 1,
            report_type= 1,
            report_submitted= datetime(2016,2,2),
            report_due= datetime(2016,2,2),
            report_doc= "doc"
        )
        
        rcsl = models.RCStatusList(
            rc_status = "Status 1",
            rc_status_definition = "rc status def")
            
        irb = models.IRBHolderLUT(
            irb_holder = "holder 1",
            irb_holder_definition= "IRB 1")
            
        rcl = models.ReviewCommitteeList(
            reviewCommittee = "rc",
            rc_description = "rc desc")
            
        pt = models.ProjectType(
            project_type = "Type 1",
            project_type_definition = "Def 1")
        
        rc.RCStatusList = rcsl
        rc.reviewCommitteeList = rcl
        p.irbHolder = irb
        p.projectType = pt
        p.reviewCommittees.append(rc)
        p.budgets.append(budget)
        p.arcReview = arcReview
        p.ucrReports.append(ucr)
        
        funding = models.Funding(
            grantStatusLUTID = 1,
            projectID = 1,
            fundingSourceLUTID = 1,
            primary_funding_source = "pfs",
            secondary_funding_source = "sfs",
            funding_number = "number",
            grant_title = "title",
            grantStatusID = 1,
            date_status = datetime(2016,2,2),
            grant_pi = 1,
            primary_chartfield = "pcf",
            secondary_chartfield = "scf"
        )
        
        fundingSourceLUT = models.FundingSourceLUT(
            fundingSource = "fs"
        )
        
        grantStatus = models.GrantStatusLUT(
            grant_status = "status"
        )
        
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "mname",
            maiden_name = "maiden_name",
            alias_fname = "alias_fname",
            alias_lname = "alias_lname",
            alias_middle_name = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vital_status = "v1"
        )
        
        projStatus = models.ProjectStatus(
            projectStatusLUTID = 1,
            projectID = 1,
            staffID = 1,
            status_date = datetime(2016,2,2),
            status_notes = "notes"
        
        )
        
        projStatusType = models.ProjectStatusLUT(
            project_status = "Status 1",
            status_definition = "status def",)
            
        projectPatient = models.ProjectPatient(
            projectID = 1,
            staffID = 1,
            ctcID = 1,
            current_age = 1,
            batch = 1,
            sitegrp = 1,
            final_code = 1,
            final_code_date = datetime(2016,2,2),
            enrollment_date = datetime(2016,2,2),
            date_coord_signed = datetime(2016,2,2),
            import_date = datetime(2016,2,2),
            final_code_staff = 1,
            enrollment_staff = 1,
            date_coord_signed_staff = datetime(2016,2,2),
            abstract_status = 1,
            abstract_status_date = datetime(2016,2,2),
            abstract_status_staff = 1,
            sent_to_abstractor = datetime(2016,2,2),
            sent_to_abstractor_staff = 1,
            abstracted_date = datetime(2016,2,2),
            abstractor_initials = "atp",
            researcher_date = datetime(2016,2,2),
            researcher_staff = 1,
            consent_link = "link",
            tracing_status = 1,
            med_record_release_signed = True,
            med_record_release_link = "link",
            med_record_release_staff = 1,
            med_record_release_date = datetime(2016,2,2),
            survey_to_researcher = datetime(2016,2,2),
            survey_to_researcher_staff = 1
        )        
        db.session.add(patient)
        db.session.add(projectPatient)
        db.session.add(projStatusType)
        db.session.add(funding)
        db.session.add(fundingSourceLUT)
        db.session.add(grantStatus)
        db.session.add(projStatus)
        db.session.add(p)
        db.session.commit()
        
class TestRoot(PopulatedDB):
    def test_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.json, {
            "version" : 0.01,
            "endpoints" : [
                "projects",
                "staff"
            ]})    

class TestArcReview(PopulatedDB):
    def test_get_arc_reviews(self):
        response = self.client.get("/api/arcreviews/")
        self.assertEqual(response.json["arcReviews"][0]["projectID"], 1)
        self.assertEqual(response.json["arcReviews"][0]["review_type"], 1)
        self.assertEqual(response.json["arcReviews"][0]["date_sent_to_reviewer"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer1"], 1)
        self.assertEqual(response.json["arcReviews"][0]["reviewer1_rec"], 1)
        self.assertEqual(response.json["arcReviews"][0]["reviewer1_sig_date"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer1_comments"], "test comment")
        self.assertEqual(response.json["arcReviews"][0]["reviewer2"], 2)
        self.assertEqual(response.json["arcReviews"][0]["reviewer2_rec"], 2)
        self.assertEqual(response.json["arcReviews"][0]["reviewer2_sig_date"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer2_comments"], "test comment")
        self.assertEqual(response.json["arcReviews"][0]["research"], 1)
        self.assertEqual(response.json["arcReviews"][0]["contact"], True)
        self.assertEqual(response.json["arcReviews"][0]["lnkage"], False)
        self.assertEqual(response.json["arcReviews"][0]["engaged"], True)
        self.assertEqual(response.json["arcReviews"][0]["non_public_data"], True)
        
    def test_get_arc_review(self):
        response = self.client.get("/api/arcreviews/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["review_type"], 1)
        self.assertEqual(response.json["date_sent_to_reviewer"], "2016-02-02")
        self.assertEqual(response.json["reviewer1"], 1)
        self.assertEqual(response.json["reviewer1_rec"], 1)
        self.assertEqual(response.json["reviewer1_sig_date"], "2016-02-02")
        self.assertEqual(response.json["reviewer1_comments"], "test comment")
        self.assertEqual(response.json["reviewer2"], 2)
        self.assertEqual(response.json["reviewer2_rec"], 2)
        self.assertEqual(response.json["reviewer2_sig_date"], "2016-02-02")
        self.assertEqual(response.json["reviewer2_comments"], "test comment")
        self.assertEqual(response.json["research"], 1)
        self.assertEqual(response.json["contact"], True)
        self.assertEqual(response.json["lnkage"], False)
        self.assertEqual(response.json["engaged"], True)
        self.assertEqual(response.json["non_public_data"], True)
        
    def test_update_arc_review(self):
        response = self.client.put("/api/arcreviews/1/", data = {
            "projectID" : 2,
            "review_type" : 2,
            "date_sent_to_reviewer" : "2016-02-03",
            "reviewer1" : 3,
            "reviewer1_rec" : 3,
            "reviewer1_sig_date" : "2016-02-03",
            "reviewer1_comments" : "test comment Updated",
            "reviewer2" : 4,
            "reviewer2_rec"  :4 ,
            "reviewer2_sig_date" : "2016-02-03",
            "reviewer2_comments" : "test comment Updated",
            "research" : 2,
            "lnkage":True,
            "contact" : False,
            "engaged" : False,
            "non_public_data" : False
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["review_type"], 2)
        self.assertEqual(response.json["date_sent_to_reviewer"], "2016-02-03")
        self.assertEqual(response.json["reviewer1"], 3)
        self.assertEqual(response.json["reviewer1_rec"], 3)
        self.assertEqual(response.json["reviewer1_sig_date"], "2016-02-03")
        self.assertEqual(response.json["reviewer1_comments"], "test comment Updated")
        self.assertEqual(response.json["reviewer2"], 4)
        self.assertEqual(response.json["reviewer2_rec"], 4)
        self.assertEqual(response.json["reviewer2_sig_date"], "2016-02-03")
        self.assertEqual(response.json["reviewer2_comments"], "test comment Updated")
        self.assertEqual(response.json["research"], 2)
        self.assertEqual(response.json["contact"], False)
        self.assertEqual(response.json["lnkage"], True)
        self.assertEqual(response.json["engaged"], False)
        self.assertEqual(response.json["non_public_data"], False)
        
    def test_delete_arc_review(self):
        response = self.client.delete("/api/arcreviews/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ArcReviewID 1 deleted")
            
class TestBudget(PopulatedDB):
    def test_get_budgets(self):
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.json["budgets"][0]["projectID"], 1)
        self.assertEqual(response.json["budgets"][0]["numPeriods"], 1)
        self.assertEqual(response.json["budgets"][0]["periodStart"], "2016-02-02")
        self.assertEqual(response.json["budgets"][0]["periodEnd"], "2016-02-02")
        self.assertEqual(response.json["budgets"][0]["periodTotal"], 1.23)
        self.assertEqual(response.json["budgets"][0]["periodComment"], "comment")
        
    def test_get_budget(self):
        response = self.client.get("/api/budgets/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["numPeriods"], 1)
        self.assertEqual(response.json["periodStart"], "2016-02-02")
        self.assertEqual(response.json["periodEnd"], "2016-02-02")
        self.assertEqual(response.json["periodTotal"], 1.23)
        self.assertEqual(response.json["periodComment"], "comment")
        
    def test_update_budget(self):
        response = self.client.put("/api/budgets/1/",data = {
            "projectID" : 2,
            "numPeriods" : 2,
            "periodStart" : "2016-02-03",
            "periodEnd" : "2016-02-03",
            "periodTotal" : 1.5,
            "periodComment" : "comment Updated"
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["numPeriods"], 2)
        self.assertEqual(response.json["periodStart"], "2016-02-03")
        self.assertEqual(response.json["periodEnd"], "2016-02-03")
        self.assertEqual(response.json["periodTotal"], 1.5)
        self.assertEqual(response.json["periodComment"], "comment Updated")
        
    def test_delete_budget(self):
        response = self.client.delete("/api/budgets/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "BudgetID 1 deleted")

class TestFunding(PopulatedDB):
    def test_get_fundings(self):
        response = self.client.get("/api/fundings/")
        self.assertEqual(response.json["Fundings"][0]["fundingID"], 1)
        self.assertEqual(response.json["Fundings"][0]["grantStatusLUTID"], 1)
        self.assertEqual(response.json["Fundings"][0]["projectID"], 1)
        self.assertEqual(response.json["Fundings"][0]["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["Fundings"][0]["primary_funding_source"], "pfs")
        self.assertEqual(response.json["Fundings"][0]["secondary_funding_source"], "sfs")
        self.assertEqual(response.json["Fundings"][0]["funding_number"], "number")
        self.assertEqual(response.json["Fundings"][0]["grant_title"], "title")
        self.assertEqual(response.json["Fundings"][0]["grantStatusID"], 1)
        self.assertEqual(response.json["Fundings"][0]["date_status"], "2016-02-02")
        self.assertEqual(response.json["Fundings"][0]["grant_pi"], 1)
        self.assertEqual(response.json["Fundings"][0]["primary_chartfield"], "pcf")
        self.assertEqual(response.json["Fundings"][0]["secondary_chartfield"], "scf")

    def test_get_funding(self):
        response = self.client.get("/api/fundings/1/")
        self.assertEqual(response.json["fundingID"], 1)
        self.assertEqual(response.json["grantStatusLUTID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["primary_funding_source"], "pfs")
        self.assertEqual(response.json["secondary_funding_source"], "sfs")
        self.assertEqual(response.json["funding_number"], "number")
        self.assertEqual(response.json["grant_title"], "title")
        self.assertEqual(response.json["grantStatusID"], 1)
        self.assertEqual(response.json["date_status"], "2016-02-02")
        self.assertEqual(response.json["grant_pi"], 1)
        self.assertEqual(response.json["primary_chartfield"], "pcf")
        self.assertEqual(response.json["secondary_chartfield"], "scf")
        
    def test_update_funding(self):
        response = self.client.put("/api/fundings/1/", data = {
            "fundingID": 1,
            "grantStatusLUTID": 2,
            "projectID": 2,
            "fundingSourceLUTID": 2,
            "primary_funding_source": "pfs Updated",
            "secondary_funding_source": "sfs Updated",
            "funding_number": "number Updated",
            "grant_title": "title Updated",
            "grantStatusID": 2,
            "date_status": "2016-02-03",
            "grant_pi": 2,
            "primary_chartfield": "pcf Updated",
            "secondary_chartfield": "scf Updated"
        })
        self.assertEqual(response.json["fundingID"], 1)
        self.assertEqual(response.json["grantStatusLUTID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["fundingSourceLUTID"], 2)
        self.assertEqual(response.json["primary_funding_source"], "pfs Updated")
        self.assertEqual(response.json["secondary_funding_source"], "sfs Updated")
        self.assertEqual(response.json["funding_number"], "number Updated")
        self.assertEqual(response.json["grant_title"], "title Updated")
        self.assertEqual(response.json["grantStatusID"], 2)
        self.assertEqual(response.json["date_status"], "2016-02-03")
        self.assertEqual(response.json["grant_pi"], 2)
        self.assertEqual(response.json["primary_chartfield"], "pcf Updated")
        self.assertEqual(response.json["secondary_chartfield"], "scf Updated")
        
    def test_delete_funding(self):
        response = self.client.delete("/api/fundings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingID 1 deleted")  
        
class TestFundingSource(PopulatedDB):
    def test_get_funding_sources(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json["FundingSources"][0]["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["FundingSources"][0]["fundingSource"], "fs")

    def test_get_funding_source(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["fundingSource"], "fs") 
        
    def test_update_funding_source(self):
        response = self.client.put("/api/fundingsources/1/", data = {
            "fundingSource" : "fs Updated",
        })
        self.assertEqual(response.json["fundingSource"], "fs Updated")
        
    def test_delete_funding_source(self):
        response = self.client.delete("/api/fundingsources/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingSourceLUTID 1 deleted")             
        
class TestGrantStatus(PopulatedDB):
    def test_get_grant_statuses(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json["GrantStatuses"][0]["grantStatusLUTID"], 1)
        self.assertEqual(response.json["GrantStatuses"][0]["grant_status"], "status")

    def test_get_grant_status(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json["grantStatusLUTID"], 1)
        self.assertEqual(response.json["grant_status"], "status")
        
    def test_update_grant_status(self):
        response = self.client.put("/api/grantstatuses/1/", data = {
            "grant_status" : "status Updated",
        })
        self.assertEqual(response.json["grant_status"], "status Updated")
        
    def test_delete_grant_status(self):
        response = self.client.delete("/api/grantstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "GrantStatusLUTID 1 deleted")     
        
class TestIRBHolder(PopulatedDB):
    def test_get_irb_holders(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json["irbHolders"][0]["irb_holder"],"holder 1")
        self.assertEqual(response.json["irbHolders"][0]["irb_holder_definition"],"IRB 1")
        
    def test_get_irb_holder(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json["irb_holder"],"holder 1")
        self.assertEqual(response.json["irb_holder_definition"],"IRB 1")
        
    def test_update_irb_holder(self):
        response = self.client.put("/api/irbholders/1/", data = {
            "irb_holder" : "holder 1 Updated",
            "irb_holder_definition" : "IRB 1 Updated"
        })
        self.assertEqual(response.json["irb_holder"],"holder 1 Updated")
        self.assertEqual(response.json["irb_holder_definition"],"IRB 1 Updated")
        
    def test_delete_irb_holder(self):
        response = self.client.delete("/api/irbholders/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "IrbHolderID 1 deleted")

class TestPatient(PopulatedDB):
    def test_get_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json["Patients"][0]["patID"], "1")
        self.assertEqual(response.json["Patients"][0]["recordID"], 1)
        self.assertEqual(response.json["Patients"][0]["ucrDistID"], 1)
        self.assertEqual(response.json["Patients"][0]["UPDBID"], 1)
        self.assertEqual(response.json["Patients"][0]["fname"], "fname")
        self.assertEqual(response.json["Patients"][0]["lname"], "lname")
        self.assertEqual(response.json["Patients"][0]["maiden_name"], "maiden_name")
        self.assertEqual(response.json["Patients"][0]["alias_fname"], "alias_fname")
        self.assertEqual(response.json["Patients"][0]["alias_lname"], "alias_lname")
        self.assertEqual(response.json["Patients"][0]["alias_middle_name"], "alias_middle")
        self.assertEqual(response.json["Patients"][0]["dob"], "2016-02-02")
        self.assertEqual(response.json["Patients"][0]["SSN"], 999999999)
        self.assertEqual(response.json["Patients"][0]["sex"], "male")
        self.assertEqual(response.json["Patients"][0]["race"], "white")
        self.assertEqual(response.json["Patients"][0]["ethnicity"], "hispanic")
        self.assertEqual(response.json["Patients"][0]["vital_status"], "v1")
        
    def test_get_patient(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json["patID"], "1")
        self.assertEqual(response.json["recordID"], 1)
        self.assertEqual(response.json["ucrDistID"], 1)
        self.assertEqual(response.json["UPDBID"], 1)
        self.assertEqual(response.json["fname"], "fname")
        self.assertEqual(response.json["lname"], "lname")
        self.assertEqual(response.json["maiden_name"], "maiden_name")
        self.assertEqual(response.json["alias_fname"], "alias_fname")
        self.assertEqual(response.json["alias_lname"], "alias_lname")
        self.assertEqual(response.json["alias_middle_name"], "alias_middle")
        self.assertEqual(response.json["dob"], "2016-02-02")
        self.assertEqual(response.json["SSN"], 999999999)
        self.assertEqual(response.json["sex"], "male")
        self.assertEqual(response.json["race"], "white")
        self.assertEqual(response.json["ethnicity"], "hispanic")
        self.assertEqual(response.json["vital_status"], "v1")
        
    def test_update_patient(self):
        response = self.client.put("/api/patients/1/", data = {
            "patID" : "2",
            "recordID" : 2,
            "ucrDistID" : 2,
            "UPDBID" : 2,
            "fname" : "fname Updated",
            "lname" : "lname Updated",
            "middle_name" : "mname Updated",
            "maiden_name" : "maiden_name Updated",
            "alias_fname" : "alias_fname Updated",
            "alias_lname" : "alias_lname Updated",
            "alias_middle_name" : "alias_middle Updated",
            "dob" : "2016-02-03",
            "SSN" : "999999990",
            "sex" : "female",
            "race" : "black",
            "ethnicity" : "non-hispanic",
            "vital_status" : "v2"
        })
        self.assertEqual(response.json["patID"], "2")
        self.assertEqual(response.json["recordID"], 2)
        self.assertEqual(response.json["ucrDistID"], 2)
        self.assertEqual(response.json["UPDBID"], 2)
        self.assertEqual(response.json["fname"], "fname Updated")
        self.assertEqual(response.json["lname"], "lname Updated")
        self.assertEqual(response.json["maiden_name"], "maiden_name Updated")
        self.assertEqual(response.json["alias_fname"], "alias_fname Updated")
        self.assertEqual(response.json["alias_lname"], "alias_lname Updated")
        self.assertEqual(response.json["alias_middle_name"], "alias_middle Updated")
        self.assertEqual(response.json["dob"], "2016-02-03")
        self.assertEqual(response.json["SSN"], 999999990)
        self.assertEqual(response.json["sex"], "female")
        self.assertEqual(response.json["race"], "black")
        self.assertEqual(response.json["ethnicity"], "non-hispanic")
        self.assertEqual(response.json["vital_status"], "v2")
        
    def test_delete_patient(self):
        response = self.client.delete("/api/patients/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatAutoID 1 deleted")      
        
class TestProject(PopulatedDB):   
    # test getting list of projects
    def test_get_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.json["projects"][0]["projectID"],1)
        self.assertEqual(response.json["projects"][0]["projectType_projectTypeID"],1)
        self.assertEqual(response.json["projects"][0]["IRBHolderLUT_irbHolderID"],1)
        self.assertEqual(response.json["projects"][0]["project_name"],"Test Project")
        self.assertEqual(response.json["projects"][0]["short_title"],"Test Project")
        self.assertEqual(response.json["projects"][0]["project_summary"],"Summary")
        self.assertEqual(response.json["projects"][0]["sop"],"sop")
        self.assertEqual(response.json["projects"][0]["UCR_proposal"],"ucr_proposal")
        self.assertEqual(response.json["projects"][0]["budget_doc"],"budget_doc")
        self.assertEqual(response.json["projects"][0]["UCR_fee"],"no")
        self.assertEqual(response.json["projects"][0]["UCR_no_fee"],"yes")
        self.assertEqual(response.json["projects"][0]["budget_end_date"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["previous_short_title"],"t short")
        self.assertEqual(response.json["projects"][0]["date_added"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["final_recruitment_report"],"report")
    # Test getting single project
    def test_get_project(self):
        response = self.client.get("/api/projects/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectType_projectTypeID"],1)
        self.assertEqual(response.json["IRBHolderLUT_irbHolderID"],1)
        self.assertEqual(response.json["project_name"],"Test Project")
        self.assertEqual(response.json["short_title"],"Test Project")
        self.assertEqual(response.json["project_summary"],"Summary")
        self.assertEqual(response.json["sop"],"sop")
        self.assertEqual(response.json["UCR_proposal"],"ucr_proposal")
        self.assertEqual(response.json["budget_doc"],"budget_doc")
        self.assertEqual(response.json["UCR_fee"],"no")
        self.assertEqual(response.json["UCR_no_fee"],"yes")
        self.assertEqual(response.json["budget_end_date"],"2016-02-02")
        self.assertEqual(response.json["previous_short_title"],"t short")
        self.assertEqual(response.json["date_added"],"2016-02-02")
        self.assertEqual(response.json["final_recruitment_report"],"report")
    # Test update project
    def test_update_project(self):
        response = self.client.put("/api/projects/1/",data = {
            "projectType_projectTypeID" : 2,
            "IRBHolderLUT_irbHolderID" : 2,
            "project_name" : "Test Project Update",
            "short_title" : "Test Project Update",
            "project_summary" : "Summary Update",
            "sop":"sop Update",
            "UCR_proposal":"ucr_proposal Update",
            "budget_doc" : "budget_doc Update",
            "UCR_fee" : "no Update",
            "UCR_no_fee" : "yes Update",
            "budget_end_date" : "2016-02-03",
            "previous_short_title" : "t short Update",
            "date_added" : "2016-02-03",
            "final_recruitment_report" : "report Update"
        })
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectType_projectTypeID"],2)
        self.assertEqual(response.json["IRBHolderLUT_irbHolderID"],2)
        self.assertEqual(response.json["project_name"],"Test Project Update")
        self.assertEqual(response.json["short_title"],"Test Project Update")
        self.assertEqual(response.json["project_summary"],"Summary Update")
        self.assertEqual(response.json["sop"],"sop Update")
        self.assertEqual(response.json["UCR_proposal"],"ucr_proposal Update")
        self.assertEqual(response.json["budget_doc"],"budget_doc Update")
        self.assertEqual(response.json["UCR_fee"],"no Update")
        self.assertEqual(response.json["UCR_no_fee"],"yes Update")
        self.assertEqual(response.json["budget_end_date"],"2016-02-03")
        self.assertEqual(response.json["previous_short_title"],"t short Update")
        self.assertEqual(response.json["date_added"],"2016-02-03")
        self.assertEqual(response.json["final_recruitment_report"],"report Update")
        
     # Test deletetion of project
    def test_delete_project(self):
        response = self.client.delete("/api/projects/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectID 1 deleted")

class TestProjectPatient(PopulatedDB):
    def test_get_project_statuses(self):
        response = self.client.get("/api/projectpatients/")
        self.assertEqual(response.json["ProjectPatients"][0]["participantID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["ctcID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["current_age"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["batch"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["sitegrp"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["final_code"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["final_code_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["enrollment_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["date_coord_signed"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["import_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["final_code_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["enrollment_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["date_coord_signed_staff"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstract_status"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstract_status_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstract_status_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["sent_to_abstractor"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["sent_to_abstractor_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstracted_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractor_initials"], "atp")
        self.assertEqual(response.json["ProjectPatients"][0]["researcher_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["researcher_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["consent_link"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["tracing_status"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_signed"], True)
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_link"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["survey_to_researcher"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["survey_to_researcher_staff"], 1)

        
    def test_get_project_patient(self):
        response = self.client.get("/api/projectpatients/1/")
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["current_age"], 1)
        self.assertEqual(response.json["batch"], 1)
        self.assertEqual(response.json["sitegrp"], 1)
        self.assertEqual(response.json["final_code"], 1)
        self.assertEqual(response.json["final_code_date"], "2016-02-02")
        self.assertEqual(response.json["enrollment_date"], "2016-02-02")
        self.assertEqual(response.json["date_coord_signed"], "2016-02-02")
        self.assertEqual(response.json["import_date"], "2016-02-02")
        self.assertEqual(response.json["final_code_staff"], 1)
        self.assertEqual(response.json["enrollment_staff"], 1)
        self.assertEqual(response.json["date_coord_signed_staff"], "2016-02-02")
        self.assertEqual(response.json["abstract_status"], 1)
        self.assertEqual(response.json["abstract_status_date"], "2016-02-02")
        self.assertEqual(response.json["abstract_status_staff"], 1)
        self.assertEqual(response.json["sent_to_abstractor"], "2016-02-02")
        self.assertEqual(response.json["sent_to_abstractor_staff"], 1)
        self.assertEqual(response.json["abstracted_date"], "2016-02-02")
        self.assertEqual(response.json["abstractor_initials"], "atp")
        self.assertEqual(response.json["researcher_date"], "2016-02-02")
        self.assertEqual(response.json["researcher_staff"], 1)
        self.assertEqual(response.json["consent_link"], "link")
        self.assertEqual(response.json["tracing_status"], 1)
        self.assertEqual(response.json["med_record_release_signed"], True)
        self.assertEqual(response.json["med_record_release_link"], "link")
        self.assertEqual(response.json["med_record_release_staff"], 1)
        self.assertEqual(response.json["med_record_release_date"], "2016-02-02")
        self.assertEqual(response.json["survey_to_researcher"], "2016-02-02")
        self.assertEqual(response.json["survey_to_researcher_staff"], 1)
        
    def test_update_project_patient(self):
        response = self.client.put("/api/projectpatients/1/", data = {
            "projectID" : 2,
            "staffID" : 2,
            "ctcID" : 2,
            "current_age" : 2,
            "batch"  : 2,
            "sitegrp" : 2,
            "final_code" : 2,
            "final_code_date" : "2016-02-03",
            "enrollment_date" : "2016-02-03",
            "date_coord_signed" : "2016-02-03",
            "import_date" : "2016-02-03",
            "final_code_staff" : 2,
            "enrollment_staff" : 2,
            "date_coord_signed_staff"  : "2016-02-03",
            "abstract_status" : 2,
            "abstract_status_date" : "2016-02-03",
            "abstract_status_staff" : 2,
            "sent_to_abstractor"  : "2016-02-03",
            "sent_to_abstractor_staff" : 2,
            "abstracted_date" : "2016-02-03",
            "abstractor_initials" : "atp Updated",
            "researcher_date" : "2016-02-03",
            "researcher_staff" : 2,
            "consent_link" : "link Updated",
            "tracing_status" : 2,
            "med_record_release_signed" : False,
            "med_record_release_link" : "link Updated",
            "med_record_release_staff" : 2,
            "med_record_release_date"  : "2016-02-03",
            "survey_to_researcher"  : "2016-02-03",
            "survey_to_researcher_staff" : 2
        })
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["current_age"], 2)
        self.assertEqual(response.json["batch"], 2)
        self.assertEqual(response.json["sitegrp"], 2)
        self.assertEqual(response.json["final_code"], 2)
        self.assertEqual(response.json["final_code_date"], "2016-02-03")
        self.assertEqual(response.json["enrollment_date"], "2016-02-03")
        self.assertEqual(response.json["date_coord_signed"], "2016-02-03")
        self.assertEqual(response.json["import_date"], "2016-02-03")
        self.assertEqual(response.json["final_code_staff"], 2)
        self.assertEqual(response.json["enrollment_staff"], 2)
        self.assertEqual(response.json["date_coord_signed_staff"], "2016-02-03")
        self.assertEqual(response.json["abstract_status"], 2)
        self.assertEqual(response.json["abstract_status_date"], "2016-02-03")
        self.assertEqual(response.json["abstract_status_staff"], 2)
        self.assertEqual(response.json["sent_to_abstractor"], "2016-02-03")
        self.assertEqual(response.json["sent_to_abstractor_staff"], 2)
        self.assertEqual(response.json["abstracted_date"], "2016-02-03")
        self.assertEqual(response.json["abstractor_initials"], "atp Updated")
        self.assertEqual(response.json["researcher_date"], "2016-02-03")
        self.assertEqual(response.json["researcher_staff"], 2)
        self.assertEqual(response.json["consent_link"], "link Updated")
        self.assertEqual(response.json["tracing_status"], 2)
        self.assertEqual(response.json["med_record_release_signed"], False)
        self.assertEqual(response.json["med_record_release_link"], "link Updated")
        self.assertEqual(response.json["med_record_release_staff"], 2)
        self.assertEqual(response.json["med_record_release_date"], "2016-02-03")
        self.assertEqual(response.json["survey_to_researcher"], "2016-02-03")
        self.assertEqual(response.json["survey_to_researcher_staff"], 2)
        
    def test_delete_project_patient(self):
        response = self.client.delete("/api/projectpatients/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ParticipantID 1 deleted")       
             
class TestProjectStatus(PopulatedDB):
    def test_get_project_statuses(self):
        response = self.client.get("/api/projectstatuses/")
        self.assertEqual(response.json["ProjectStatuses"][0]["projectStatusLUTID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["status_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectStatuses"][0]["status_notes"], "notes")
        
    def test_get_project_status(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json["projectStatusLUTID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["status_date"], "2016-02-02")
        self.assertEqual(response.json["status_notes"], "notes")
        
    def test_update_project_status(self):
        response = self.client.put("/api/projectstatuses/1/", data = {
            "projectStatusLUTID" : 2,
            "projectID": 2,
            "staffID" : 2,
            "status_date" : "2016-02-03",
            "status_notes": "notes Updated"
        })
        self.assertEqual(response.json["projectStatusLUTID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["status_date"], "2016-02-03")
        self.assertEqual(response.json["status_notes"], "notes Updated")
        
    def test_delete_project_status(self):
        response = self.client.delete("/api/projectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusID 1 deleted")       
        
class TestProjectStatusType(PopulatedDB):
    def test_get_project_status_types(self):
        response = self.client.get("/api/projectstatustypes/")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatusTypeID"], 1)
        self.assertEqual(response.json["ProjectStatusTypes"][0]["project_status"], "Status 1")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["status_definition"], "status def")
        
    def test_get_project_status_type(self):
        response = self.client.get("/api/projectstatustypes/1/")
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["project_status"], "Status 1")
        self.assertEqual(response.json["status_definition"], "status def")
        
    def test_update_project_status_type(self):
        response = self.client.put("/api/projectstatustypes/1/", data = {
            "project_status" : "Status 1 Updated",
            "status_definition" : "status def Updated"
        })
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["project_status"], "Status 1 Updated")
        self.assertEqual(response.json["status_definition"], "status def Updated")
        
    def test_delete_project_status_type(self):
        response = self.client.delete("/api/projectstatustypes/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusTypeID 1 deleted")            
 
class TestProjectType(PopulatedDB):
    def test_get_project_types(self):
        response = self.client.get("/api/projecttypes/")
        self.assertEqual(response.json["ProjectTypes"][0]["project_type"], "Type 1")
        self.assertEqual(response.json["ProjectTypes"][0]["project_type_definition"], "Def 1")
        
    def test_get_project_type(self):
        response = self.client.get("/api/projecttypes/1/")
        self.assertEqual(response.json["project_type"], "Type 1")
        self.assertEqual(response.json["project_type_definition"], "Def 1")
        
    def test_update_project_type(self):
        response = self.client.put("/api/projecttypes/1/", data = {
            "project_type" : "2",
            "project_type_definition" : "type def Updated"
        })
        self.assertEqual(response.json["project_type"], "2")
        self.assertEqual(response.json["project_type_definition"], "type def Updated")
        
    def test_delete_project_type(self):
        response = self.client.delete("/api/projecttypes/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectTypeID 1 deleted")      
 
class TestRCStatusList(PopulatedDB):
    def test_get_rcStatusList(self):
        response = self.client.get("/api/rcstatuslist/")
        self.assertEqual(response.json["RCStatusList"][0]["rcStatusID"], 1)
        self.assertEqual(response.json["RCStatusList"][0]["rc_status"], "Status 1")
        self.assertEqual(response.json["RCStatusList"][0]["rc_status_definition"], "rc status def")
        
    def test_get_rcStatus(self):
        response = self.client.get("/api/rcstatuslist/1/")
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rc_status"], "Status 1")
        self.assertEqual(response.json["rc_status_definition"], "rc status def")
        
    def test_update_rcStatus(self):
        response = self.client.put("/api/rcstatuslist/1/", data = {
            "rc_status" : "Status 1 Updated",
            "rc_status_definition" : "rc status def Updated"
        })
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rc_status"], "Status 1 Updated")
        self.assertEqual(response.json["rc_status_definition"], "rc status def Updated")
        
    def test_delete_rcStatusList(self):
        response = self.client.delete("/api/rcstatuslist/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCStatusListID 1 deleted")
                     
class TestReviewCommittee(PopulatedDB):
    def test_get_review_committees(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json['reviewCommittees'][0]["project_projectID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["RCStatusList_rc_StatusID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["reviewCommitteeList_rcListID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["review_committee_number"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["date_initial_review"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["date_expires"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["rc_note"], "rc_note")
        self.assertEqual(response.json['reviewCommittees'][0]["rc_protocol"], "rc_proto")
        self.assertEqual(response.json['reviewCommittees'][0]["rc_approval"], "rc_approval")
        
    def test_get_review_committees(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json["project_projectID"], 1)
        self.assertEqual(response.json["RCStatusList_rc_StatusID"], 1)
        self.assertEqual(response.json["reviewCommitteeList_rcListID"], 1)
        self.assertEqual(response.json["review_committee_number"], "1")
        self.assertEqual(response.json["date_initial_review"], "2016-02-02")
        self.assertEqual(response.json["date_expires"], "2016-02-02")
        self.assertEqual(response.json["rc_note"], "rc_note")
        self.assertEqual(response.json["rc_protocol"], "rc_proto")
        self.assertEqual(response.json["rc_approval"], "rc_approval")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommittees/1/", data = {
            "project_projectID" : 2,
            "RCStatusList_rc_StatusID": 2,
            "reviewCommitteeList_rcListID": 2,
            "review_committee_number":"2",
            "date_initial_review":"2016-02-03",
            "date_expires" : "2016-02-03",
            "rc_note" : "rc_note Updated",
            "rc_protocol" : "rc_proto Updated",
            "rc_approval":"rc_approval Updated"
        })
        self.assertEqual(response.json["project_projectID"], 2)
        self.assertEqual(response.json["RCStatusList_rc_StatusID"], 2)
        self.assertEqual(response.json["reviewCommitteeList_rcListID"], 2)
        self.assertEqual(response.json["review_committee_number"], "2")
        self.assertEqual(response.json["date_initial_review"], "2016-02-03")
        self.assertEqual(response.json["date_expires"], "2016-02-03")
        self.assertEqual(response.json["rc_note"], "rc_note Updated")
        self.assertEqual(response.json["rc_protocol"], "rc_proto Updated")
        self.assertEqual(response.json["rc_approval"], "rc_approval Updated")
        
    def test_delete_review_committee(self):
        response = self.client.delete("/api/reviewcommittees/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ReviewCommitteeID 1 deleted")
        
class TestReviewCommitteeList(PopulatedDB):
    def test_get_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json["reviewCommitteeList"][0]["reviewCommittee"], "rc")
        self.assertEqual(response.json["reviewCommitteeList"][0]["rc_description"], "rc desc")
        
    def test_get_review_committee_list(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["reviewCommittee"], "rc")
        self.assertEqual(response.json["rc_description"], "rc desc")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommitteelist/1/", data = {
            "reviewCommittee" : "rc Updated",
            "rc_description" : "rc desc Updated"
            })
        self.assertEquals(response.json["reviewCommittee"],"rc Updated")
        self.assertEquals(response.json["rc_description"],"rc desc Updated")
        
    def test_delete_review_committee_list(self):
        response = self.client.delete("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCListID 1 deleted")

class TestUCRReport(PopulatedDB):
    def test_get_ucr_report(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json["ucrReports"][0]["projectID"],1)
        self.assertEqual(response.json["ucrReports"][0]["report_type"],1)
        self.assertEqual(response.json["ucrReports"][0]["report_submitted"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["report_due"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["report_doc"],"doc")
        
    def test_get_ucr_report(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["report_type"],1)
        self.assertEqual(response.json["report_submitted"],"2016-02-02")
        self.assertEqual(response.json["report_due"],"2016-02-02")
        self.assertEqual(response.json["report_doc"],"doc")
        
    def test_update_ucr_report(self):
        response = self.client.put("/api/ucrreports/1/", data = {
            "projectID" : 2,
            "report_type": 2,
            "report_submitted": "2016-02-03",
            "report_due": "2016-02-03",
            "report_doc": "doc Updated"
        })
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["report_type"],2)
        self.assertEqual(response.json["report_submitted"],"2016-02-03")
        self.assertEqual(response.json["report_due"],"2016-02-03")
        self.assertEqual(response.json["report_doc"],"doc Updated")
        
    def test_delete_ucr_report(self):
        response = self.client.delete("/api/ucrreports/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "UcrReportID 1 deleted")
        
        
        
if __name__ == '__main__':
    unittest.main()