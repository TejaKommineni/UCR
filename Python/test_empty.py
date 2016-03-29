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
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(p)
        db.session.commit()

    def test_empty_arc_review(self):
        response = self.client.get("/api/arcreviews/")
        self.assertEqual(response.json, {"arcReviews" : []})
        
    def test_arc_review_no_id(self):
        response = self.client.get("/api/arcreviews/1/")
        self.assertEqual(response.json, {"Error" : "ArcReviewID 1 not found"})
    
    def test_create_arc_review(self):
        response = self.client.post("/api/arcreviews/", data = {
            "projectID" : 1,
            "reviewType" : 1,
            "dateSentToReviewer" : "2016-02-02",
            "reviewer1" : 1,
            "reviewer1Rec" : 1,
            "reviewer1SigDate" : "2016-02-02",
            "reviewer1Comments" : "test comment",
            "reviewer2" : 2,
            "reviewer2Rec"  :2 ,
            "reviewer2SigDate" : "2016-02-02",
            "reviewer2Comments" : "2016-02-02",
            "research" : 1,
            "linkage":False,
            "contact" : True,
            "engaged" : True,
            "nonPublicData" : True,
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"arcReviewID" : 1})
            
class TestBudget(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(p)
        db.session.commit()

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
            "periodComment" : "comment",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(budgetID=1))

class TestContact(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        contactType = models.ContactTypeLUT(
            contactDefinition = "def"
        )
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        informant = models.Informant(
            patientID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            informantPrimary = "informant_primary",
            informantRelationship = "informant_relationship",
            notes = "notes"
        )
        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatus = 1,
            physicianStatusDate = datetime(2016,2,2),
        )

        project1 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )

        ctc1 = models.CTC(
            patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        projectPatient = models.ProjectPatient(
            projectID = 1,
            staffID = 1,
            ctcID = 1,
            currentAge = 1,
            batch = 1,
            siteGrp = 1,
            finalCode = 1,
            finalCodeDate = datetime(2016,2,2),
            enrollmentDate = datetime(2016,2,2),
            dateCoordSigned = datetime(2016,2,2),
            importDate = datetime(2016,2,2),
            finalCodeStaffID = 1,
            enrollmentStaffID = 1,
            dateCoordSignedStaffID = 1,
            abstractStatus = 1,
            abstractStatusDate = datetime(2016,2,2),
            abstractStatusStaffID = 1,
            sentToAbstractorDate = datetime(2016,2,2),
            sentToAbstractorStaffID = 1,
            abstractedDate = datetime(2016,2,2),
            abstractorStaffID = 1,
            researcherDate = datetime(2016,2,2),
            researcherStaffID = 1,
            consentLink = "link",
            medRecordReleaseSigned = True,
            medRecordReleaseLink = "link",
            medRecordReleaseStaffID = 1,
            medRecordReleaseDate = datetime(2016,2,2),
            surveyToResearcher = datetime(2016,2,2),
            surveyToResearcherStaffID = 1
        )

        db.session.add(contactType)
        db.session.add(facility1)
        db.session.add(patient)
        db.session.add(informant)
        db.session.add(physician)
        db.session.add(staff)
        db.session.add(project1)
        db.session.add(ctc1)
        db.session.add(staff)
        db.session.add(projectPatient)
        db.session.commit()

    def test_empty_contact(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json, {"Contacts" : [] })
        
    def test_contact_no_id(self):
        response = self.client.get('/api/contacts/1/')
        self.assertEqual(response.json, {"Error" : "ContactID 1 not found"})
        
    def test_create_contact(self):
        response = self.client.post("/api/contacts/", data = {
            "contactTypeLUTID" : 1,
            "projectPatientID" : 1,
            "staffID" : 1,
            "informantID" : 1,
            "facilityID" : 1,
            "physicianID" : 1,
            "description" : "desc",
            "contactDate" : "2016-02-02",
            "initials" : "atp",
            "notes" : "notes",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(contactID=1))
        
class TestContactType(BlankDB):
    def test_empty_contact_type(self):
        response = self.client.get("/api/contacttypes/")
        self.assertEqual(response.json, {"ContactTypes" : [] })
        
    def test_contact_type_no_id(self):
        response = self.client.get('/api/contacttypes/1/')
        self.assertEqual(response.json, {"Error" : "ContactTypeID 1 not found"})
        
    def test_create_contact_type(self):
        response = self.client.post("/api/contacttypes/", data = {
            "contactDefinition" : "contactDefinition",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(contactTypeID=1))
                
class TestContactInfoStatus(BlankDB):
    def test_empty_contact_info_status(self):
        response = self.client.get("/api/contactinfostatuses/")
        self.assertEqual(response.json, {"ContactInfoStatuses" : [] })
        
    def test_contact_info_status_no_id(self):
        response = self.client.get('/api/contactinfostatuses/1/')
        self.assertEqual(response.json, {"Error" : "ContactInfoStatusID 1 not found"})
        
    def test_create_contact_info_status(self):
        response = self.client.post("/api/contactinfostatuses/", data = {
            "contactInfoStatus" : "status",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(contactInfoStatusID=1))
        
class TestContactInfoSource(BlankDB):
    def test_empty_contact_info_source(self):
        response = self.client.get("/api/contactinfosources/")
        self.assertEqual(response.json, {"ContactInfoSources" : [] })
        
    def test_contact_info_source_no_id(self):
        response = self.client.get('/api/contactinfosources/1/')
        self.assertEqual(response.json, {"Error" : "ContactInfoSourceID 1 not found"})
        
    def test_create_contact_info_source(self):
        response = self.client.post("/api/contactinfosources/", data = {
            "contactInfoSource" : "source",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(contactInfoSourceID=1))

class TestCTC(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        db.session.add(patient)
        db.session.commit()

    def test_empty_ctc(self):
        response = self.client.get("/api/ctcs/")
        self.assertEqual(response.json, {"CTCs" : [] })
        
    def test_ctc_no_id(self):
        response = self.client.get('/api/ctcs/1/')
        self.assertEqual(response.json, {"Error" : "CtcID 1 not found"})
        
    def test_create_ctc(self):
        response = self.client.post("/api/ctcs/", data = {
            "patientID" : 1,
            "dxDate" : "2016-02-02",
            "site" : 1,
            "histology" : "histology",
            "behavior" : "behavior",
            "ctcSequence" : "sequence",
            "stage" : "stage",
            "dxAge" : 1,
            "dxStreet1" : "street",
            "dxStreet2" : "street2",
            "dxCity" : "city",
            "dxState" : "state",
            "dxZip" : 99999,
            "dxCounty" : "county",
            "dnc" : "dnc",
            "dncReason" : "dnc_reason",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(ctcID=1))

class TestCTCFacility(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )

        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )
        ctc1 = models.CTC(
           patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        db.session.add(facility1)
        db.session.add(patient)
        db.session.add(ctc1)
        db.session.commit()

    def test_empty_ctc_facility(self):
        response = self.client.get("/api/ctcfacilities/")
        self.assertEqual(response.json, dict(CTCFacilities = []))
   
    def test_ctc_facility_no_id(self):
        response = self.client.get("/api/ctcfacilities/1/")
        self.assertEqual(response.json, {"Error" : "CTCFacilityID 1 not found"})

    def test_create_ctc_facility(self):
        response = self.client.post("/api/ctcfacilities/", data = {
            "ctcID" : 1,
            "facilityID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"CTCFacilityID": 1})  
        
class TestFacilityPhone(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        phoneType = models.PhoneTypeLUT(
            phoneType = "cell"
        )

        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )
        db.session.add(phoneType)
        db.session.add(facility1)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_facility_phone(self):
        response = self.client.get("/api/facilityphones/")
        self.assertEqual(response.json, dict(FacilityPhones = []))
   
    def test_facility_phone_no_id(self):
        response = self.client.get("/api/facilityphones/1/")
        self.assertEqual(response.json, {"Error" : "FacilityPhoneID 1 not found"})

    def test_create_facility_phone(self):
        response = self.client.post("/api/facilityphones/", data = {
            "contactInfoSourceID" : 1,
            "facilityID" : 1,
            "contactInfoStatusID" : 1,
            "clinicName" : "clinic",
            "phoneTypeID" : 1,
            "phoneNumber" : "phone",
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"facilityPhoneID": 1})  

class TestFacility(BlankDB):
    def test_empty_facility_phone(self):
        response = self.client.get("/api/facilities/")
        self.assertEqual(response.json, dict(Facilities = []))
   
    def test_facility_phone_no_id(self):
        response = self.client.get("/api/facilities/1/")
        self.assertEqual(response.json, {"Error" : "FacilityID 1 not found"})

    def test_create_facility_phone(self):
        response = self.client.post("/api/facilities/", data = {
            "facilityName" : "name",
            "contactFirstName" : "fname:",
            "contactLastName" : "lname",
            "facilityStatus" : 1,
            "facilityStatusDate" : "2016-02-02",
            "contact2FirstName" : "fname",
            "contact2LastName" : "lname",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"facilityID": 1})  

class TestFacilityAddress(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        db.session.add(facility1)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_facility_address(self):
        response = self.client.get("/api/facilityaddresses/")
        self.assertEqual(response.json, dict(FacilityAddresses = []))
   
    def test_facility_address_no_id(self):
        response = self.client.get("/api/facilityaddresses/1/")
        self.assertEqual(response.json, {"Error" : "FacilityAddressID 1 not found"})

    def test_create_facility_address(self):
        response = self.client.post("/api/facilityaddresses/", data = {
            "contactInfoSourceID" : 1,
            "facilityID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "state" : "state",
            "zip" : "zip",
            "addressStatus" : 1,
            "addressStatusDate" : "2016-02-02",
            "addressStatusSource" : "s1",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"facilityAddressID": 1})
        
class TestFunding(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        grantStatus = models.GrantStatusLUT(
            grantStatus = "status"
        )

        fundingSource = models.FundingSourceLUT(
            fundingSource = "source"
        )

        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(grantStatus)
        db.session.add(fundingSource)
        db.session.add(p)
        db.session.commit()

    def test_empty_funding(self):
        response = self.client.get("/api/fundings/")
        self.assertEqual(response.json, dict(Fundings = []))
   
    def test_funding_no_id(self):
        response = self.client.get("/api/fundings/1/")
        self.assertEqual(response.json, {"Error" : "FundingID 1 not found"})

    def test_create_funding(self):
        response = self.client.post("/api/fundings/", data = {
            "grantStatusID": 1,
            "projectID": 1,
            "fundingSourceID": 1,
            "primaryFundingSource" : "fs 1",
            "secondaryFundingSource": "fs 2",
            "fundingNumber": "number",
            "grantTitle" : "title",
            "dateStatus" : "2016-02-02",
            "grantPi": 1,
            "primaryChartfield" : "chartfield 1",
            "secondaryChartfield" : "chartfield 2",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"fundingID": 1})
        
class TestFundingSource(BlankDB):

    def test_empty_funding_source(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json, dict(FundingSources = []))
   
    def test_funding_source__no_id(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json, {"Error" : "FundingSourceID 1 not found"})

    def test_create_funding_source(self):
        response = self.client.post("/api/fundingsources/", data = {
            "fundingSource" : "fs",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"fundingSourceID": 1})
        
class TestGrantStatus(BlankDB):

    def test_empty_grant_status(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json, dict(GrantStatuses = []))
   
    def test_grant_status__no_id(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json, {"Error" : "GrantStatusID 1 not found"})

    def test_create_grant_status(self):
        response = self.client.post("/api/grantstatuses/", data = {
            "grantStatus" : "status",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"grantStatusID": 1})

class TestHumanSubjectTraining(BlankDB):
    def test_empty_human_subject_training(self):
        response = self.client.get("/api/humansubjecttrainings/")
        self.assertEqual(response.json, dict(HumanSubjectTrainings = []))
   
    def test_human_subject_training__no_id(self):
        response = self.client.get("/api/humansubjecttrainings/1/")
        self.assertEqual(response.json, {"Error" : "HumanSubjectTrainingID 1 not found"})

    def test_create_human_subject_training(self):
        response = self.client.post("/api/humansubjecttrainings/", data = {
            "trainingType" : "type",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"humanSubjectTrainingID": 1})

class TestIncentive(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        project_type1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        project1 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        staff = models.Staff(
           firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )

        ctc1 = models.CTC(
            patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        projectPatient = models.ProjectPatient(
            projectID = 1,
            staffID = 1,
            ctcID = 1,
            currentAge = 1,
            batch = 1,
            siteGrp = 1,
            finalCode = 1,
            finalCodeDate = datetime(2016,2,2),
            enrollmentDate = datetime(2016,2,2),
            dateCoordSigned = datetime(2016,2,2),
            importDate = datetime(2016,2,2),
            finalCodeStaffID = 1,
            enrollmentStaffID = 1,
            dateCoordSignedStaffID = 1,
            abstractStatus = 1,
            abstractStatusDate = datetime(2016,2,2),
            abstractStatusStaffID = 1,
            sentToAbstractorDate = datetime(2016,2,2),
            sentToAbstractorStaffID = 1,
            abstractedDate = datetime(2016,2,2),
            abstractorStaffID = 1,
            researcherDate = datetime(2016,2,2),
            researcherStaffID = 1,
            consentLink = "link",
            medRecordReleaseSigned = True,
            medRecordReleaseLink = "link",
            medRecordReleaseStaffID = 1,
            medRecordReleaseDate = datetime(2016,2,2),
            surveyToResearcher = datetime(2016,2,2),
            surveyToResearcherStaffID = 1
        )
        patientProjectStatusType = models.PatientProjectStatusLUT(
            statusDescription = "desc"
        )
        db.session.add(patient)
        db.session.add(irb_holder1)
        db.session.add(project_type1)
        db.session.add(project1)
        db.session.add(staff)
        db.session.add(ctc1)
        db.session.add(projectPatient)
        db.session.add(patientProjectStatusType)
        db.session.commit()

    def test_empty_incentive(self):
        response = self.client.get("/api/incentives/")
        self.assertEqual(response.json, dict(Incentives = []))

    def test_incentive__no_id(self):
        response = self.client.get("/api/incentives/1/")
        self.assertEqual(response.json, {"Error" : "IncentiveID 1 not found"})

    def test_create_incentive(self):
        response = self.client.post("/api/incentives/", data = {
            "projectPatientID" : 1,
            "incentiveDescription": "desc",
            "incentiveDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"incentiveID": 1})

class TestInformant(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
           patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_informant(self):
        response = self.client.get("/api/informants/")
        self.assertEqual(response.json, dict(Informants = []))
   
    def test_informant_no_id(self):
        response = self.client.get("/api/informants/1/")
        self.assertEqual(response.json, {"Error" : "InformantID 1 not found"})

    def test_create_informant(self):
        response = self.client.post("/api/informants/", data = {
            "patientID" : 1,
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "middle_name",
            "informantPrimary" : "informant_primary",
            "informantRelationship" : "informant_relationship",
            "notes" : "notes",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"informantID": 1})              
        
class TestInformantAddress(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )
        informant = models.Informant(
            patientID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            informantPrimary = "informant_primary",
            informantRelationship = "informant_relationship",
            notes = "notes"
        )

        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.add(informant)
        db.session.commit()
        
    def test_empty_informant_address(self):
        response = self.client.get("/api/informantaddresses/")
        self.assertEqual(response.json, dict(InformantAddresses = []))
   
    def test_informant_address_no_id(self):
        response = self.client.get("/api/informantaddresses/1/")
        self.assertEqual(response.json, {"Error" : "InformantAddressID 1 not found"})

    def test_create_informant_address(self):
        response = self.client.post("/api/informantaddresses/", data = {
            "contactInfoSourceID" : 1,
            "informantID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "state" : "state",
            "zip" : "zip",
            "addressStatus" : 1,
            "addressStatusDate" : "2016-02-02",
            "addressStatusSource" : "s1",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"informantAddressID": 1})        
        
class TestInformantPhone(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        phoneType = models.PhoneTypeLUT(
            phoneType = "cell"
        )
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )
        informant = models.Informant(
            patientID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            informantPrimary = "informant_primary",
            informantRelationship = "informant_relationship",
            notes = "notes"
        )
        db.session.add(phoneType)
        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.add(informant)
        db.session.commit()

    def test_empty_informant_phone(self):
        response = self.client.get("/api/informantphones/")
        self.assertEqual(response.json, dict(InformantPhones = []))
   
    def test_informant_phone_no_id(self):
        response = self.client.get("/api/informantphones/1/")
        self.assertEqual(response.json, {"Error" : "InformantPhoneID 1 not found"})

    def test_create_informant_phone(self):
        response = self.client.post("/api/informantphones/", data = {
            "contactInfoSourceID" : 1,
            "informantID" : 1,
            "contactInfoStatusID" : 1,
            "phoneNumber" : "phone",
            "phoneTypeID" : 1,
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"informantPhoneID": 1})       
        
class TestIRBHolder(BlankDB):
    def test_empty_irb_holder(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json, {"irbHolders" : []})
    
    def test_irb_holder_no_id(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json, {"Error" : "IrbHolderID 1 not found"})
        
    def test_create_irb_holder(self):
        response = self.client.post("/api/irbholders/", data = {
            "holder" : "test holder",
            "holderDefinition" : "test holder def",
            "versionID" : 1,
            })
        self.assertEqual(response.json, dict(irbHolderID=1))

class TestLog(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        phaseStatus = models.PhaseStatus(
            phaseStatus = "status",
            phaseDescription = "desc"
        )

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )

        logSubject = models.LogSubjectLUT(
            logSubject = "subject"
        )

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(p)
        db.session.add(staff)
        db.session.add(logSubject)
        db.session.add(phaseStatus)
        db.session.commit()

    def test_empty_log(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.json, {"Logs" : []})
    
    def test_log_no_id(self):
        response = self.client.get("/api/logs/1/")
        self.assertEqual(response.json, {"Error" : "LogID 1 not found"})
        
    def test_create_log(self):
        response = self.client.post("/api/logs/", data = {
            "logSubjectID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "phaseStatusID" : 1,
            "note" : "note",
            "date" : "2016-02-02",
            "versionID" : 1,
            })
        self.assertEqual(response.json, dict(logID=1))
        
class TestLogSubject(BlankDB):
    def test_empty_log_subject(self):
        response = self.client.get("/api/logsubjects/")
        self.assertEqual(response.json, {"LogSubjects" : []})
    
    def test_log_subject_no_id(self):
        response = self.client.get("/api/logsubjects/1/")
        self.assertEqual(response.json, {"Error" : "LogSubjectID 1 not found"})
        
    def test_create_log_subject(self):
        response = self.client.post("/api/logsubjects/", data = {
            "logSubject" : "subject",
            "versionID" : 1,
            })
        self.assertEqual(response.json, dict(logSubjectID=1))
        
class TestPatient(BlankDB):
    def test_empty_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json, dict(Patients = []))
   
    def test_patient_no_id(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json, {"Error" : "PatientID 1 not found"})

    def test_create_patient(self):
        response = self.client.post("/api/patients/", data = {
            "patID" : 1,
            "recordID" : 1,
            "ucrDistID" : 1,
            "UPDBID" : 1,
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "mname",
            "maidenName" : "madien_name",
            "aliasFirstName" : "alias_fname",
            "aliasLastName" : "alias_lname",
            "aliasMiddleName" : "alias_middle",
            "dob" : "2016-02-02",
            "SSN" : "999999999",
            "sex" : "male",
            "race" : "white",
            "ethnicity" : "hispanic",
            "vitalStatus" : "v1",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"patientID": 1})

class TestPatientAddress(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_patient_address(self):
        response = self.client.get("/api/patientaddresses/")
        self.assertEqual(response.json, dict(PatientAddresses = []))
   
    def test_patient_address_no_id(self):
        response = self.client.get("/api/patientaddresses/1/")
        self.assertEqual(response.json, {"Error" : "PatAddressID 1 not found"})

    def test_create_patient_address(self):
        response = self.client.post("/api/patientaddresses/", data = {
            "contactInfoSourceID" : 1,
            "patientID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "state" : "state",
            "zip" : "zip",
            "addressStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"patAddressID": 1})

class TestPatientEmail(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_patient_email(self):
        response = self.client.get("/api/patientemails/")
        self.assertEqual(response.json, dict(PatientEmails = []))
   
    def test_patient_email_no_id(self):
        response = self.client.get("/api/patientemails/1/")
        self.assertEqual(response.json, {"Error" : "EmailID 1 not found"})

    def test_create_patient_email(self):
        response = self.client.post("/api/patientemails/", data = {
            "contactInfoSourceID" : 1,
            "patientID" : 1,
            "contactInfoStatusID" : 1,
            "email" : "email",
            "emailStatus" : 1,
            "emailSource" : 1,
            "emailStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"emailID": 1})

class TestPatientPhone(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        phoneType = models.PhoneTypeLUT(
            phoneType = "cell"
        )
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )
        db.session.add(phoneType)
        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_patient_phone(self):
        response = self.client.get("/api/patientphones/")
        self.assertEqual(response.json, dict(PatientPhones = []))
   
    def test_patient_phone_no_id(self):
        response = self.client.get("/api/patientphones/1/")
        self.assertEqual(response.json, {"Error" : "PatPhoneID 1 not found"})

    def test_create_phone_phone(self):
        response = self.client.post("/api/patientphones/", data = {
            "contactInfoSourceID" : 1,
            "patientID" : 1,
            "contactInfoStatusID" : 1,
            "phoneTypeID": 1,
            "phoneNumber" : "phone",
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"patPhoneID": 1})       

class TestPatientProjectStatus(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        project_type1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        project1 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )

        ctc1 = models.CTC(
            patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        projectPatient = models.ProjectPatient(
            projectID = 1,
            staffID = 1,
            ctcID = 1,
            currentAge = 1,
            batch = 1,
            siteGrp = 1,
            finalCode = 1,
            finalCodeDate = datetime(2016,2,2),
            enrollmentDate = datetime(2016,2,2),
            dateCoordSigned = datetime(2016,2,2),
            importDate = datetime(2016,2,2),
            finalCodeStaffID = 1,
            enrollmentStaffID = 1,
            dateCoordSignedStaffID = 1,
            abstractStatus = 1,
            abstractStatusDate = datetime(2016,2,2),
            abstractStatusStaffID = 1,
            sentToAbstractorDate = datetime(2016,2,2),
            sentToAbstractorStaffID = 1,
            abstractedDate = datetime(2016,2,2),
            abstractorStaffID = 1,
            researcherDate = datetime(2016,2,2),
            researcherStaffID = 1,
            consentLink = "link",
            medRecordReleaseSigned = True,
            medRecordReleaseLink = "link",
            medRecordReleaseStaffID = 1,
            medRecordReleaseDate = datetime(2016,2,2),
            surveyToResearcher = datetime(2016,2,2),
            surveyToResearcherStaffID = 1
        )
        patientProjectStatusType = models.PatientProjectStatusLUT(
            statusDescription = "desc"
        )
        db.session.add(patient)
        db.session.add(irb_holder1)
        db.session.add(project_type1)
        db.session.add(project1)
        db.session.add(staff)
        db.session.add(ctc1)
        db.session.add(projectPatient)
        db.session.add(patientProjectStatusType)
        db.session.commit()

    def test_empty_patient_project_status(self):
        response = self.client.get("/api/patientprojectstatuses/")
        self.assertEqual(response.json, dict(PatientProjectStatuses = []))
   
    def test_patient_project_status_no_id(self):
        response = self.client.get("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json, {"Error" : "PatientProjectStatusID 1 not found"})

    def test_create_patient_project_status(self):
        response = self.client.post("/api/patientprojectstatuses/", data = {
            "patientProjectStatusTypeID" : 1,
            "projectPatientID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"patientProjectStatusID": 1})
        
class TestPatientProjectStatusLUT(BlankDB):
    def test_empty_patient_project_status_type(self):
        response = self.client.get("/api/patientprojectstatustypes/")
        self.assertEqual(response.json, dict(PatientProjectStatusTypes = []))
   
    def test_patient_project_status_type_no_id(self):
        response = self.client.get("/api/patientprojectstatustypes/1/")
        self.assertEqual(response.json, {"Error" : "PatientProjectStatusTypeID 1 not found"})

    def test_create_patient_project_status_type(self):
        response = self.client.post("/api/patientprojectstatustypes/", data = {
            "statusDescription" : "desc",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"patientProjectStatusTypeID": 1})

class TestPhaseStatus(BlankDB):
    def test_empty_phase_status(self):
        response = self.client.get("/api/phasestatuses/")
        self.assertEqual(response.json, dict(PhaseStatuses = []))
   
    def test_phase_status_no_id(self):
        response = self.client.get("/api/phasestatuses/1/")
        self.assertEqual(response.json, {"Error" : "LogPhaseID 1 not found"})

    def test_create_phase_status(self):
        response = self.client.post("/api/phasestatuses/", data = {
            "phaseStatus" : "status",
            "phaseDescription" : "description",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"logPhaseID": 1})

class TestPhoneType(BlankDB):
    def test_emtpy_phone_type(self):
        response = self.client.get("/api/phonetypes/")
        self.assertEqual(response.json, {"PhoneTypes": []})

    def test_phone_type_no_id(self):
        response = self.client.get("/api/phonetypes/1/")
        self.assertEqual(response.json, {"Error" : "PhoneTypeID 1 not found"})

    def test_create_phone_type(self):
        response = self.client.post("/api/phonetypes/", data = {
            "phoneType" : "phoneType",
            "versionID" : 1,
        })
        self.assertEqual(response.json, dict(phoneTypeID=1))

class TestPhysician(BlankDB):

    def test_empty_physician(self):
        response = self.client.get("/api/physicians/")
        self.assertEqual(response.json, dict(Physicians = []))
   
    def test_physician_no_id(self):
        response = self.client.get("/api/physicians/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianID 1 not found"})

    def test_create_physician(self):
        response = self.client.post("/api/physicians/", data = {
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "middle_name",
            "credentials" : "credentials",
            "specialty" : "specialty",
            "aliasFirstName" : "alias_fname",
            "aliasLastName" : "alias_lname",
            "aliasMiddleName" : "alias_middle_name",
            "physicianStatus" : 1,
            "physicianStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"physicianID": 1})

class TestPhysicianAddress(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatus = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add(physician)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_physician_address(self):
        response = self.client.get("/api/physicianaddresses/")
        self.assertEqual(response.json, dict(PhysicianAddresses = []))
   
    def test_physician_address_no_id(self):
        response = self.client.get("/api/physicianaddresses/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianAddressID 1 not found"})

    def test_create_physician_address(self):
        response = self.client.post("/api/physicianaddresses/", data = {
            "contactInfoSourceID" : 1,
            "physicianID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "state" : "state",
            "zip" : "zip",
            "addressStatus" : 1,
            "addressStatusDate" : "2016-02-02",
            "addressStatusSource" : "s1",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"physicianAddressID": 1})

class TestPhysicianEmail(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        db.session.add(patient)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_physician_email(self):
        response = self.client.get("/api/physicianemails/")
        self.assertEqual(response.json, dict(PhysicianEmails = []))

    def test_physician_email_no_id(self):
        response = self.client.get("/api/physicianemails/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianEmailID 1 not found"})

    def test_create_physician_email(self):
        response = self.client.post("/api/physicianemails/", data = {
            "contactInfoSourceID" : 1,
            "physicianID" : 1,
            "contactInfoStatusID" : 1,
            "email" : "email",
            "emailStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"physicianEmailID": 1})

class TestPhysicianFacility(BlankDB):

    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )
        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatus = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add(facility1)
        db.session.add(physician)
        db.session.commit()

    def test_empty_physician_facility(self):
        response = self.client.get("/api/physicianfacilities/")
        self.assertEqual(response.json, dict(PhysicianFacilities = []))
   
    def test_physician_facility_no_id(self):
        response = self.client.get("/api/physicianfacilities/1/")
        self.assertEqual(response.json, {"Error" : "PhysFacilityID 1 not found"})

    def test_create_physician_facility(self):
        response = self.client.post("/api/physicianfacilities/", data = {
            "facilityID" : 1,
            "physicianID" : 1,
            "physFacilityStatus" : 1,
            "physFacilityStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"physFacilityID": 1})       
         
class TestPhysicianPhone(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        phoneType = models.PhoneTypeLUT(
            phoneType = "cell"
        )
        contactInfoStatus = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatus = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add(phoneType)
        db.session.add(physician)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.commit()

    def test_empty_physician_phone(self):
        response = self.client.get("/api/physicianphones/")
        self.assertEqual(response.json, dict(PhysicianPhones = []))
   
    def test_physician_phone_no_id(self):
        response = self.client.get("/api/physicianphones/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianPhoneID 1 not found"})

    def test_create_phone_phone(self):
        response = self.client.post("/api/physicianphones/", data = {
            "contactInfoSourceID" : 1,
            "physicianID" : 1,
            "contactInfoStatusID" : 1,
            "phoneNumber" : "phone",
            "phoneTypeID" : 1,
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"physicianPhoneID": 1})       
        
class TestPhysicianToCTC(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        ctc = models.CTC(
            patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatus = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add(patient)
        db.session.add(physician)
        db.session.add(ctc)
        db.session.commit()

    def test_empty_physician_to_ctc(self):
        response = self.client.get("/api/physiciantoctcs/")
        self.assertEqual(response.json, dict(PhysicianToCTCs = []))
   
    def test_physician_to_ctc_no_id(self):
        response = self.client.get("/api/physiciantoctcs/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianCTCID 1 not found"})

    def test_create_physician_to_ctc(self):
        response = self.client.post("/api/physiciantoctcs/", data = {
            "physicianID" : 1,
            "ctcID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"physicianCTCID": 1})

class TestPreApplication(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(p)
        db.session.commit()

    def test_empty_pre_application(self):
        response = self.client.get("/api/preapplications/")
        self.assertEqual(response.json, dict(PreApplications = []))
   
    def test_pre_application_no_id(self):
        response = self.client.get("/api/preapplications/1/")
        self.assertEqual(response.json, {"Error" : "PreApplicationID 1 not found"})

    def test_create_pre_application(self):
        response = self.client.post("/api/preapplications/", data = {
            "projectID" : 1,
            "piFirstName" : "pi_fname",
            "piLastName" : "pi_lname",
            "piEmail" : "pi_email",
            "piPhone" : "pi_phone",
            "contactFirstName" : "contact_fname",
            "contactLastName" : "contact_lname",
            "contactPhone" : "contact_phone",
            "contactEmail" : "contact_email",
            "institution" : "institution",
            "institution2" : "institution2",
            "uid" : "uid",
            "udoh" : 1,
            "projectTitle" : "project_title",
            "purpose" : "purpose",
            "irb0" : True,
            "irb1" : True,
            "irb2" : True,
            "irb3" : True,
            "irb4" : True,
            "otherIrb" : "other_irb",
            "updb" : True,
            "ptContact" : True,
            "startDate" : "2016-02-02",
            "link" : True,
            "deliveryDate" : "2016-02-02",
            "description" : "description",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"preApplicationID": 1})
                
class TestProject(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        db.session.add(pt1)
        db.session.add(irb_holder1)
        db.session.commit()

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
    def test_create_project(self):
        response = self.client.post("/api/projects/", data = {
            "projectTypeID" : 1,
            "irbHolderID" : 1,
            "projectTitle" : "Test Project",
            "shortTitle" : "Test Project",
            "projectSummary" : "Summary",
            "sop":"sop",
            "ucrProposal":"ucr_proposal",
            "budgetDoc" : "budget_doc",
            "ucrFee" : "no",
            "ucrNoFee" : "yes",
            "previousShortTitle" : "t short",
            "dateAdded" : "2016-02-02",
            "finalRecruitmentReport" : "report",
            "ongoingContact" : True,
            "activityStartDate" : "2016-02-02",
            "activityEndDate" : "2016-02-02",
            "versionID" : 1,})
        self.assertEqual(response.json,dict(projectID=1))

class TestProjectPatient(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )

        project1 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        ctc = models.CTC(
            patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        db.session.add(pt1)
        db.session.add(irb_holder1)
        db.session.add(staff)
        db.session.add(project1)
        db.session.add(patient)
        db.session.add(ctc)
        db.session.commit()

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
            "currentAge" : 1,
            "batch"  : 1,
            "siteGrp" : 1,
            "finalCode" : 1,
            "finalCodeDate" : "2016-02-02",
            "enrollmentDate" : "2016-02-02",
            "dateCoordSigned" : "2016-02-02",
            "importDate" : "2016-02-02",
            "finalCodeStaffID" : 1,
            "enrollmentStaffID" : 1,
            "dateCoordSignedStaffID"  : 1,
            "abstractStatus" : 1,
            "abstractStatusDate" : "2016-02-02",
            "abstractStatusStaffID" : 1,
            "sentToAbstractorDate"  : "2016-02-02",
            "sentToAbstractorStaffID" : 1,
            "abstractedDate" : "2016-02-02",
            "abstractorStaffID" : 1,
            "researcherDate" : "2016-02-02",
            "researcherStaffID" : 1,
            "consentLink" : "consent",
            "medRecordReleaseSigned" : True,
            "medRecordReleaseLink" : "link",
            "medRecordReleaseStaffID" : 1,
            "medRecordReleaseDate"  : "2016-02-02",
            "surveyToResearcher"  : "2016-02-02",
            "surveyToResearcherStaffID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"participantID": 1})

class TestProjectStaff(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )
        staffRole = models.StaffRoleLUT(
            staffRole = "role",
            staffRoleDescription = "desc"
        )

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(staff)
        db.session.add(staffRole)
        db.session.add(p)
        db.session.commit()

    def test_empty_project_staff(self):
        response = self.client.get("/api/projectstaff/")
        self.assertEqual(response.json, {"ProjectStaff" : []})
    
    def test_project_staff_no_id(self):
        response = self.client.get("/api/projectstaff/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStaffID 1 not found"})
        
    def test_create_project_staff(self):
        response = self.client.post("/api/projectstaff/", data = {
            "staffRoleID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "role" : 1,
            "datePledge" : "2016-02-02",
            "dateRevoked" : "2016-02-02",
            "contact" : "yes",
            "inactive" : "no",
            "humanSubjectTrainingExp" : "2016-02-02",
            "humanSubjectTrainingTypeID" : 1,
            "studyRole" : 1,
            "versionID" : 1,
            })
        self.assertEqual(response.json, dict(projectStaffID=1))
        
class TestProjectStatus(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )
        projStatusType = models.ProjectStatusLUT(
            projectStatus = "Status 1",
            projectStatusDefinition = "status def"
        )

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(staff)
        db.session.add(projStatusType)
        db.session.add(p)
        db.session.commit()

    def test_empty_project_status(self):
        response = self.client.get("/api/projectstatuses/")
        self.assertEqual(response.json, dict(ProjectStatuses = []))
   
    def test_project_status_no_id(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStatusID 1 not found"})

    def test_create_project_status(self):
        response = self.client.post("/api/projectstatuses/", data = {
            "projectStatusTypeID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "statusDate" : "2016-02-02",
            "statusNotes" : "note",
            "versionID" : 1,
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
            "projectStatus" : "Status 1",
            "projectStatusDefinition" : "status def",
            "versionID" : 1,
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
            "projectType" : 1,
            "projectTypeDefinition" : "type def",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"projectTypeID": 1})
 
class ReviewCommitteeStatusLUT(BlankDB):
    # Test for empty RCStatusList
    def test_empty_rcStatusList(self):
        response = self.client.get("/api/reviewcommitteestatuses/")
        self.assertEqual(response.json, dict(ReviewCommitteeStatuses = []))
    # Test for rcStatusList not found    
    def test_rcStatusList_no_id(self):
        response = self.client.get("/api/reviewcommitteestatuses/1/")
        self.assertEqual(response.json, {"Error" : "ReviewCommitteeStatusID 1 not found"})
    # Test create RCStatusList
    def test_create_rcStatusList(self):
        response = self.client.post("/api/reviewcommitteestatuses/", data = {
            "reviewCommitteeStatus" : "Status 1",
            "reviewCommitteeStatusDefinition" : "rc status def",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"reviewCommitteeStatusID": 1})

class TestReviewCommittee(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        rcsl = models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus = "Status 1",
            reviewCommitteeStatusDefinition = "rc status def")

        rcl1 = models.ReviewCommitteeLUT(
            reviewCommittee = "rc 1",
            reviewCommitteeDescription = "rc desc 1")

        db.session.add(pt1)
        db.session.add(irb_holder1)
        db.session.add(p)
        db.session.add(rcsl)
        db.session.add(rcl1)
        db.session.commit()

    def test_empty_review_committee(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json, dict(reviewCommittees = []))
        
    def test_review_committee_no_id(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json, {"Error": "ReviewCommitteeID 1 not found"})
        
    def test_create_review_committee(self):
        response = self.client.post("/api/reviewcommittees/", data = {
            "projectID" : 1,
            "reviewCommitteeStatusID": 1,
            "reviewCommitteeLUTID": 1,
            "reviewCommitteeNumber":"1",
            "dateInitialReview":"2016-02-02",
            "dateExpires" : "2016-02-02",
            "rcNote" : "rc_note",
            "rcProtocol" : "rc_proto",
            "rcApproval":"rc_approval",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"reviewCommitteeID" : 1})
        
class TestReviewCommitteeLUT(BlankDB):
    def test_empty_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json, dict(ReviewCommitteeList = []))
        
    def test_review_committee_list_no_id(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json, {"Error": "ReviewCommitteeID 1 not found"})
        
    def test_create_review_committee_list(self):
        response = self.client.post("/api/reviewcommitteelist/", data = {
            "reviewCommittee" : "rc test",
            "reviewCommitteeDescription" : "rc desc",
            "versionID" : 1,
            })
        self.assertEqual(response.json, {"reviewCommitteeID" : 1 })

class TestStaff(BlankDB):
    def test_empty_staff(self):
        response = self.client.get("/api/staff/")
        self.assertEqual(response.json, dict(Staff = []))
        
    def test_staff_no_id(self):
        response = self.client.get("/api/staff/1/")
        self.assertEqual(response.json, {"Error": "StaffID 1 not found"})
        
    def test_create_staff(self):
        response = self.client.post("/api/staff/", data = {
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "middle_name",
            "email" : "email",
            "phoneNumber" : "phone",
            "phoneComment" : "phoneComment",
            "institution" : "institution",
            "department" : "department",
            "position" : "position",
            "credentials" : "credentials",
            "street" : "street",
            "city" : "city",
            "state" : "state",
            "humanSubjectTrainingExp" : "2016-02-02",
            "ucrRole" : 1,
            "versionID" : 1,
            })
        self.assertEqual(response.json, {"staffID" : 1 })

class TestStaffRole(BlankDB):
    def test_empty_staff_role(self):
        response = self.client.get("/api/staffroles/")
        self.assertEqual(response.json, dict(StaffRoles = []))
        
    def test_staff_role_no_id(self):
        response = self.client.get("/api/staffroles/1/")
        self.assertEqual(response.json, {"Error": "StaffRoleID 1 not found"})
        
    def test_create_staff_role(self):
        response = self.client.post("/api/staffroles/", data = {
            "staffRole" : "role",
            "staffRoleDescription" : "desc",
            "versionID" : 1,
            })
        self.assertEqual(response.json, {"staffRoleID" : 1 })
                
class TestStaffTraining(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )
        humanSubjectTraining = models.HumanSubjectTrainingLUT(
            trainingType = "type"
        )
        db.session.add(staff)
        db.session.add(humanSubjectTraining)
        db.session.commit()

    def test_empty_staff_training(self):
        response = self.client.get("/api/stafftrainings/")
        self.assertEqual(response.json, dict(StaffTrainings = []))
        
    def test_staff_training_no_id(self):
        response = self.client.get("/api/stafftrainings/1/")
        self.assertEqual(response.json, {"Error": "StaffTrainingID 1 not found"})
        
    def test_create_staff_training(self):
        response = self.client.post("/api/stafftrainings/", data = {
            "staffID" : 1,
            "humanSubjectTrainingID" : 1,
            "dateTaken" : "2016-02-02",
            "dateExpires" : "2016-02-02",
            "versionID" : 1,
            })
        self.assertEqual(response.json, {"staffTrainingID" : 1 })        
        
class TestTracing(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "mname",
            maidenName = "maiden_name",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vitalStatus = "v1"
        )

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        project_type1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        project1 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            humanSubjectTrainingExp = datetime(2016,2,2),
            ucrRole = 1
        )

        ctc1 = models.CTC(
            patientID = 1,
            dxDate = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctcSequence = "sequence",
            stage = "stage",
            dxAge = 1,
            dxStreet1 = "street1",
            dxStreet2 = "street2",
            dxCity = "city",
            dxState = "state",
            dxZip = 99999,
            dxCounty = "county",
            dnc = "dnc",
            dncReason = "dnc_reason"
        )

        projectPatient = models.ProjectPatient(
            projectID = 1,
            staffID = 1,
            ctcID = 1,
            currentAge = 1,
            batch = 1,
            siteGrp = 1,
            finalCode = 1,
            finalCodeDate = datetime(2016,2,2),
            enrollmentDate = datetime(2016,2,2),
            dateCoordSigned = datetime(2016,2,2),
            importDate = datetime(2016,2,2),
            finalCodeStaffID = 1,
            enrollmentStaffID = 1,
            dateCoordSignedStaffID = 1,
            abstractStatus = 1,
            abstractStatusDate = datetime(2016,2,2),
            abstractStatusStaffID = 1,
            sentToAbstractorDate = datetime(2016,2,2),
            sentToAbstractorStaffID = 1,
            abstractedDate = datetime(2016,2,2),
            abstractorStaffID = 1,
            researcherDate = datetime(2016,2,2),
            researcherStaffID = 1,
            consentLink = "link",
            medRecordReleaseSigned = True,
            medRecordReleaseLink = "link",
            medRecordReleaseStaffID = 1,
            medRecordReleaseDate = datetime(2016,2,2),
            surveyToResearcher = datetime(2016,2,2),
            surveyToResearcherStaffID = 1
        )

        tracingSource = models.TracingSourceLUT(
            description = "desc"
        )

        db.session.add(patient)
        db.session.add(irb_holder1)
        db.session.add(project_type1)
        db.session.add(project1)
        db.session.add(staff)
        db.session.add(ctc1)
        db.session.add(projectPatient)
        db.session.add(tracingSource)
        db.session.commit()

    def test_empty_tracing(self):
        response = self.client.get("/api/tracings/")
        self.assertEqual(response.json, dict(Tracings = []))
        
    def test_tracing_no_id(self):
        response = self.client.get("/api/tracings/1/")
        self.assertEqual(response.json, {"Error": "TracingID 1 not found"})
        
    def test_create_tracing(self):
        response = self.client.post("/api/tracings/", data = {
            "tracingSourceID" : 1,
            "projectPatientID" : 1,
            "date" : "2016-02-02",
            "staff" : 1,
            "notes" : "notes",
            "versionID" : 1,
            })
        self.assertEqual(response.json, {"tracingID" : 1 })        
        
class TestTracingSource(BlankDB):
    def test_empty_tracing_source(self):
        response = self.client.get("/api/tracingsources/")
        self.assertEqual(response.json, dict(TracingSources = []))
        
    def test_tracing_source_no_id(self):
        response = self.client.get("/api/tracingsources/1/")
        self.assertEqual(response.json, {"Error": "TracingSourceID 1 not found"})
        
    def test_create_tracing_source(self):
        response = self.client.post("/api/tracingsources/", data = {
            "description" : "desc",
            "versionID" : 1,
            })
        self.assertEqual(response.json, {"tracingSourceID" : 1 })
             
class TestUCRReport(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        p = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectTitle = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report",
            ongoingContact = True,
            activityStartDate = datetime(2016,2,2),
            activityEndDate = datetime(2016,2,2))

        db.session.add(pt1)
        db.session.add(irb_holder1)
        db.session.add(p)
        db.session.commit()

    def test_empty_ucr_report(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json, dict(ucrReports = []))
        
    def test_ucr_report_no_id(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json, {"Error": "UcrReportID 1 not found"})
        
    def test_create_ucr_report(self):
        response = self.client.post("/api/ucrreports/", data = {
            "projectID" : 1,
            "reportType" : 1,
            "reportSubmitted" : "2016-02-02",
            "reportDue" : "2016-02-02",
            "reportDoc" : "doc",
            "versionID" : 1,
        })
        self.assertEqual(response.json, {"ucrReportID" : 1})
        
if __name__ == '__main__':
    unittest.main()
    