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
        self.populate_db2()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db2(self):
        irb_holder1 = models.IRBHolderLUT(
            holder = "holder 1",
            holderDefinition= "IRB 1")

        irb_holder2 = models.IRBHolderLUT(
            holder = "holder 2",
            holderDefinition= "IRB 2")

        project_type1 = models.ProjectType(
            projectType = "Type 1",
            projectTypeDefinition = "Def 1")

        project_type2 = models.ProjectType(
            projectType = "Type 2",
            projectTypeDefinition = "Def 2")

        project1 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectName = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            budgetEndDate = datetime(2016,2,2),
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report")

        project2 = models.Project(
            projectTypeID = 1,
            irbHolderID = 1,
            projectName = "Test Project",
            shortTitle = "Test Project",
            projectSummary = "Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc = "budget_doc",
            ucrFee = "no",
            ucrNoFee = "yes",
            budgetEndDate = datetime(2016,2,2),
            previousShortTitle = "t short",
            dateAdded = datetime(2016,2,2),
            finalRecruitmentReport = "report")

        budget1 = models.Budget(
            projectID = 1,
            numPeriods = 1,
            periodStart = datetime(2016,2,2),
            periodEnd = datetime(2016,2,2),
            periodTotal = 1.23,
            periodComment = "comment")

        rcsl = models.RCStatusList(
            rcStatus = "Status 1",
            rcStatusDefinition = "rc status def")

        rcs2 = models.RCStatusList(
            rcStatus = "Status 2",
            rcStatusDefinition = "rc status def 2")

        rcl1 = models.ReviewCommitteeList(
            reviewCommittee = "rc 1",
            rcDescription = "rc desc 1")

        rcl2 = models.ReviewCommitteeList(
            reviewCommittee = "rc 2",
            rcDescription = "rc des 2c")

        rc = models.ReviewCommittee(
            projectID=1,
            rcStatusID=1,
            rcListID=1,
            reviewCommitteeNumber="1",
            dateInitialReview=datetime(2016,2,2),
            dateExpires = datetime(2016,2,2),
            rcNote = "rc_note",
            rcProtocol = "rc_proto",
            rcApproval="rc_approval")

        ucr = models.UCRReport(
            projectID = 1,
            reportType= 1,
            reportSubmitted= datetime(2016,2,2),
            reportDue= datetime(2016,2,2),
            reportDoc= "doc"
        )
        arcReview = models.ArcReview(
            projectID = 1,
            reviewType = 1,
            dateSentToReviewer = datetime(2016,2,2),
            reviewer1 = 1,
            reviewer1Rec = 1,            reviewer1SigDate = datetime(2016,2,2),
            reviewer1Comments = "test comment",
            reviewer2 = 2,
            reviewer2Rec  =2 ,
            reviewer2SigDate = datetime(2016,2,2),
            reviewer2Comments = "test comment",
            research = 1,
            lnkage=False,
            contact = True,
            engaged = True,
            nonPublicData = True)

        grantStatus1 = models.GrantStatusLUT(
            grantStatus = "status"
        )

        fundingSource1 = models.FundingSourceLUT(
            fundingSource = "source"
        )

        grantStatus2 = models.GrantStatusLUT(
            grantStatus = "status2"
        )

        fundingSource2 = models.FundingSourceLUT(
            fundingSource = "source2"
        )

        funding = models.Funding(
            grantStatusID = 1,
            projectID = 1,
            fundingSourceID = 1,
            primaryFundingSource = "pfs",
            secondaryFundingSource = "sfs",
            fundingNumber = "number",
            grantTitle = "title",
            dateStatus = datetime(2016,2,2),
            grantPi = 1,
            primaryChartfield = "pcf",
            secondaryChartfield = "scf"
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
        staff2 = models.Staff(
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

        projStatusType1 = models.ProjectStatusLUT(
            projectStatus = "Status 1",
            projectStatusDefinition = "status def"
        )
        projStatusType2 = models.ProjectStatusLUT(
            projectStatus = "Status 2",
            projectStatusDefinition = "status def 2"
        )

        projStatus = models.ProjectStatus(
            projectStatusTypeID = 1,
            projectID = 1,
            staffID = 1,
            statusDate = datetime(2016,2,2),
            statusNotes = "notes"
        )

        preApp = models.PreApplication(
            projectID = 1,
            piFirstName = "pi_fname",
            piLastName = "pi_lname",
            piEmail = "pi_email",
            piPhone = "pi_phone",
            contactFirstName = "contact_fname",
            contactLastName = "contact_lname",
            contactPhone = "contact_phone",
            contactEmail = "contact_email",
            institution = "institution",
            institution2 = "institution2",
            uid = "uid",
            udoh = 1,
            projectTitle = "project_title",
            purpose = "purpose",
            irb0 = True,
            irb1 = True,
            irb2 = True,
            irb3 = True,
            irb4 = True,
            otherIrb = "other_irb",
            updb = True,
            ptContact = True,
            startDate = datetime(2016,2,2),
            link = True,
            deliveryDate = datetime(2016,2,2),
            description = "description"
        )

        phaseStatus1 = models.PhaseStatus(
            phaseStatus = "status",
            phaseDescription = "desc"
        )

        phaseStatus2 = models.PhaseStatus(
            phaseStatus = "status",
            phaseDescription = "desc"
        )
        logSubject1 = models.LogSubjectLUT(
            logSubject = "subject"
        )
        logSubject2 = models.LogSubjectLUT(
            logSubject = "subject"
        )
        log = models.Log(
            logSubjectID = 1,
            projectID = 1,
            staffID = 1,
            phaseStatusID = 1,
            note = "note",
            date = datetime(2016,2,2)
        )
        projectStaff = models.ProjectStaff(
            staffRoleID = 1,
            projectID = 1,
            staffID = 1,
            role = 1,
            datePledge = datetime(2016,2,2),
            dateRevoked = datetime(2016,2,2),
            contact = "yes",
            inactive = "no",
            humanSubjectTrainingExp = datetime(2016,2,2),
            humanSubjectTrainingTypeID = 1,
            studyRole = 1
        )
        staffRole1 = models.StaffRoleLUT(
            staffRole = "role",
            staffRoleDescription = "desc"
        )
        staffRole2 = models.StaffRoleLUT(
            staffRole = "role",
            staffRoleDescription = "desc"
        )
        staffTraining = models.StaffTraining(
            staffID = 1,
            humanSubjectTrainingID = 1,
            dateTaken = datetime(2016,2,2),
            dateExpires = datetime(2016,2,2)
        )
        humanSubjectTraining1 = models.HumanSubjectTrainingLUT(
            trainingType = "type"
        )
        humanSubjectTraining2 = models.HumanSubjectTrainingLUT(
            trainingType = "type"
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
        patient2 = models.Patient(
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

        contactInfoStatus1 = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource1 = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )
        contactInfoStatus2 = models.ContactInfoStatusLUT(
            contactInfoStatus = "status"
        )

        contactInfoSource2 = models.ContactInfoSourceLUT(
            contactInfoSource = "source"
        )

        patientAddress = models.PatientAddress(
            contactInfoSourceID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            addressStatus = 1,
            addressStatusDate = datetime(2016,2,2),
            addressStatusSource = "s1"
        )

        patientEmail = models.PatientEmail(
            contactInfoSourceID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            email = "email",
            emailStatus = 1,
            emailSource = 1,
            emailStatusDate = datetime(2016,2,2)
        )
        patientPhone = models.PatientPhone(
            contactInfoSourceID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            phoneNumber = "phone",
            phoneStatus = 1,
            phoneSource = "s1",
            phoneStatusDate = datetime(2016,2,2)
        )
        informant1 = models.Informant(
            patientID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            informantPrimary = "informant_primary",
            informantRelationship = "informant_relationship",
            notes = "notes"
        )
        informant2 = models.Informant(
            patientID = 1,
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            informantPrimary = "informant_primary",
            informantRelationship = "informant_relationship",
            notes = "notes"
        )
        informantAddress = models.InformantAddress(
            contactInfoSourceID = 1,
            informantID = 1,
            contactInfoStatusID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            addressStatus = 1,
            addressStatusDate = datetime(2016,2,2),
            addressStatusSource = "s1"
        )
        informantPhone = models.InformantPhone(
            contactInfoSourceID = 1,
            informantID = 1,
            contactInfoStatusID = 1,
            phoneNumber = "phone",
            phoneStatus = 1,
            phoneSource = "s1",
            phoneStatusDate = datetime(2016,2,2)
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
        ctc2 = models.CTC(
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
            finalCodeStaff = 1,
            enrollmentStaff = 1,
            dateCoordSignedStaff = datetime(2016,2,2),
            abstractStatus = 1,
            abstractStatusDate = datetime(2016,2,2),
            abstractStatusStaff = 1,
            sentToAbstractorDate = datetime(2016,2,2),
            sentToAbstractorStaff = 1,
            abstractedDate = datetime(2016,2,2),
            abstractorInitials = "atp",
            researcherDate = datetime(2016,2,2),
            researcherStaff = 1,
            consentLink = "link",
            tracingStatus = 1,
            medRecordReleaseSigned = True,
            medRecordReleaseLink = "link",
            medRecordReleaseStaff = 1,
            medRecordReleaseDate = datetime(2016,2,2),
            surveyToResearcher = datetime(2016,2,2),
            surveyToResearcherStaff = 1
        )

        projectPatient2 = models.ProjectPatient(
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
            finalCodeStaff = 1,
            enrollmentStaff = 1,
            dateCoordSignedStaff = datetime(2016,2,2),
            abstractStatus = 1,
            abstractStatusDate = datetime(2016,2,2),
            abstractStatusStaff = 1,
            sentToAbstractorDate = datetime(2016,2,2),
            sentToAbstractorStaff = 1,
            abstractedDate = datetime(2016,2,2),
            abstractorInitials = "atp",
            researcherDate = datetime(2016,2,2),
            researcherStaff = 1,
            consentLink = "link",
            tracingStatus = 1,
            medRecordReleaseSigned = True,
            medRecordReleaseLink = "link",
            medRecordReleaseStaff = 1,
            medRecordReleaseDate = datetime(2016,2,2),
            surveyToResearcher = datetime(2016,2,2),
            surveyToResearcherStaff = 1)

        tracingSource1 = models.TracingSourceLUT(
            description = "desc"
        )
        tracingSource2 = models.TracingSourceLUT(
            description = "desc"
        )
        tracing = models.Tracing(
            tracingSourceID = 1,
            projectPatientID = 1,
            date = datetime(2016,2,2),
            staff = 1,
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
            email = "email"
        )

        physician2 = models.Physician(
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
            email = "email"
        )
        physicianAddress = models.PhysicianAddress(
            contactInfoSourceID = 1,
            physicianID = 1,
            contactInfoStatusID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            addressStatus = 1,
            addressStatusDate = datetime(2016,2,2),
            addressStatusSource = "s1"
        )
        physicianPhone = models.PhysicianPhone(
            contactInfoSourceID = 1,
            physicianID = 1,
            contactInfoStatusID = 1,
            phoneNumber = "phone",
            phoneType = "phone_type",
            phoneStatus = 1,
            phoneSource = "s1",
            phoneStatusDate = datetime(2016,2,2)
        )
        physicianToCTC = models.PhysicianToCTC(
            physicianID = 1,
            ctcID = 1
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
        facility2 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )
        facilityAddress = models.FacilityAddress(
            contactInfoSourceID = 1,
            facilityID = 1,
            contactInfoStatusID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            addressStatus = 1,
            addressStatusDate = datetime(2016,2,2),
            addressStatusSource = "s1"
        )

        facilityPhone = models.FacilityPhone(
            contactInfoSourceID = 1,
            facilityID = 1,
            contactInfoStatusID = 1,
            clinicName = "clinic",
            phoneType = "cell",
            phoneNumber = "phone",
            phoneStatus = 1,
            phoneSource = "s1",
            phoneStatusDate = datetime(2016,2,2)
        )
        patientProjectStatusType1 = models.PatientProjectStatusLUT(
            statusDescription = "desc"
        )
        patientProjectStatusType2 = models.PatientProjectStatusLUT(
            statusDescription = "desc"
        )
        patientProjectStatus = models.PatientProjectStatus(
            patientProjectStatusTypeID =1,
            projectPatientID = 1,
        )
        physicianFacility = models.PhysicianFacility(
            facilityID = 1,
            physicianID = 1,
            physFacilityStatus = "s1",
            physFacilityStatusDate = datetime(2016,2,2)
        )
        contactType1 = models.ContactTypeLUT(
            contactDefinition = "def"
        )
        contactType2 = models.ContactTypeLUT(
            contactDefinition = "def"
        )
        contact = models.Contact(
            contactTypeLUTID = 1,
            projectPatientID = 1,
            staffID = 1,
            informantID = 1,
            facilityID = 1,
            physicianID = 1,
            description = "desc",
            contactDate = datetime(2016,2,2),
            initials = "atp",
            notes = "notes"
        )
        ctcFacility = models.CTCFacility(
            ctcID = 1,
            facilityID = 1
        )

        db.session.add(contactInfoSource1)
        db.session.add(contactInfoSource2)
        db.session.add(contactInfoStatus1)
        db.session.add(contactInfoStatus2)
        db.session.add(humanSubjectTraining1)
        db.session.add(humanSubjectTraining2)
        db.session.add(staffRole1)
        db.session.add(staffRole2)
        db.session.add(logSubject1)
        db.session.add(logSubject2)
        db.session.add(phaseStatus1)
        db.session.add(phaseStatus2)
        db.session.add(projStatusType1)
        db.session.add(projStatusType2)
        db.session.add(projStatus)
        db.session.add(staff)
        db.session.add(staff2)
        db.session.add(grantStatus1)
        db.session.add(grantStatus2)
        db.session.add(fundingSource1)
        db.session.add(fundingSource2)
        db.session.add(funding)
        db.session.add(irb_holder1)
        db.session.add(irb_holder2)
        db.session.add(project_type1)
        db.session.add(project_type2)
        db.session.add(project1)
        db.session.add(project2)
        db.session.add(budget1)
        db.session.add(rcsl)
        db.session.add(rcs2)
        db.session.add(rcl1)
        db.session.add(rcl2)
        db.session.add(rc)
        db.session.add(ucr)
        db.session.add(arcReview)
        db.session.add(preApp)
        db.session.add(log)
        db.session.add(projectStaff)
        db.session.add(staffTraining)
        db.session.add(patient)
        db.session.add(patient2)
        db.session.add(patientAddress)
        db.session.add(patientEmail)
        db.session.add(patientPhone)
        db.session.add(informant1)
        db.session.add(informant2)
        db.session.add(informantAddress)
        db.session.add(informantPhone)
        db.session.add(ctc1)
        db.session.add(ctc2)
        db.session.add(projectPatient)
        db.session.add(projectPatient2)
        db.session.add(tracingSource1)
        db.session.add(tracingSource2)
        db.session.add(tracing)
        db.session.add(physician)
        db.session.add(physician2)
        db.session.add(physicianAddress)
        db.session.add(physicianPhone)
        db.session.add(physicianToCTC)
        db.session.add(facility1)
        db.session.add(facility2)
        db.session.add(facilityAddress)
        db.session.add(facilityPhone)
        db.session.add(patientProjectStatusType1)
        db.session.add(patientProjectStatusType2)
        db.session.add(patientProjectStatus)
        db.session.add(physicianFacility)
        db.session.add(contactType1)
        db.session.add(contactType2)
        db.session.add(contact)
        db.session.add(ctcFacility)
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
        self.assertEqual(response.json["arcReviews"][0]["reviewType"], 1)
        self.assertEqual(response.json["arcReviews"][0]["dateSentToReviewer"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer1"], 1)
        self.assertEqual(response.json["arcReviews"][0]["reviewer1Rec"], 1)
        self.assertEqual(response.json["arcReviews"][0]["reviewer1SigDate"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer1Comments"], "test comment")
        self.assertEqual(response.json["arcReviews"][0]["reviewer2"], 2)
        self.assertEqual(response.json["arcReviews"][0]["reviewer2Rec"], 2)
        self.assertEqual(response.json["arcReviews"][0]["reviewer2SigDate"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer2Comments"], "test comment")
        self.assertEqual(response.json["arcReviews"][0]["research"], 1)
        self.assertEqual(response.json["arcReviews"][0]["contact"], True)
        self.assertEqual(response.json["arcReviews"][0]["lnkage"], False)
        self.assertEqual(response.json["arcReviews"][0]["engaged"], True)
        self.assertEqual(response.json["arcReviews"][0]["nonPublicData"], True)
        
    def test_get_arc_review(self):
        response = self.client.get("/api/arcreviews/1/")
        print(response.json)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["reviewType"], 1)
        self.assertEqual(response.json["dateSentToReviewer"], "2016-02-02")
        self.assertEqual(response.json["reviewer1"], 1)
        self.assertEqual(response.json["reviewer1Rec"], 1)
        self.assertEqual(response.json["reviewer1SigDate"], "2016-02-02")
        self.assertEqual(response.json["reviewer1Comments"], "test comment")
        self.assertEqual(response.json["reviewer2"], 2)
        self.assertEqual(response.json["reviewer2Rec"], 2)
        self.assertEqual(response.json["reviewer2SigDate"], "2016-02-02")
        self.assertEqual(response.json["reviewer2Comments"], "test comment")
        self.assertEqual(response.json["research"], 1)
        self.assertEqual(response.json["contact"], True)
        self.assertEqual(response.json["lnkage"], False)
        self.assertEqual(response.json["engaged"], True)
        self.assertEqual(response.json["nonPublicData"], True)
        
    def test_update_arc_review(self):
        response = self.client.put("/api/arcreviews/1/", data = {
            "projectID" : 2,
            "reviewType" : 2,
            "dateSentToReviewer" : "2016-02-03",
            "reviewer1" : 3,
            "reviewer1Rec" : 3,
            "reviewer1SigDate" : "2016-02-03",
            "reviewer1Comments" : "test comment Updated",
            "reviewer2" : 4,
            "reviewer2Rec"  :4 ,
            "reviewer2SigDate" : "2016-02-03",
            "reviewer2Comments" : "test comment Updated",
            "research" : 2,
            "lnkage":True,
            "contact" : False,
            "engaged" : False,
            "nonPublicData" : False
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["reviewType"], 2)
        self.assertEqual(response.json["dateSentToReviewer"], "2016-02-03")
        self.assertEqual(response.json["reviewer1"], 3)
        self.assertEqual(response.json["reviewer1Rec"], 3)
        self.assertEqual(response.json["reviewer1SigDate"], "2016-02-03")
        self.assertEqual(response.json["reviewer1Comments"], "test comment Updated")
        self.assertEqual(response.json["reviewer2"], 4)
        self.assertEqual(response.json["reviewer2Rec"], 4)
        self.assertEqual(response.json["reviewer2SigDate"], "2016-02-03")
        self.assertEqual(response.json["reviewer2Comments"], "test comment Updated")
        self.assertEqual(response.json["research"], 2)
        self.assertEqual(response.json["contact"], False)
        self.assertEqual(response.json["lnkage"], True)
        self.assertEqual(response.json["engaged"], False)
        self.assertEqual(response.json["nonPublicData"], False)
        
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

class TestContact(PopulatedDB):
    def test_get_contacts(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json["Contacts"][0]["contactID"], 1)
        self.assertEqual(response.json["Contacts"][0]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["Contacts"][0]["projectPatientID"], 1)
        self.assertEqual(response.json["Contacts"][0]["staffID"], 1)
        self.assertEqual(response.json["Contacts"][0]["informantID"], 1)
        self.assertEqual(response.json["Contacts"][0]["facilityID"], 1)
        self.assertEqual(response.json["Contacts"][0]["physicianID"], 1)
        self.assertEqual(response.json["Contacts"][0]["description"], "desc")
        self.assertEqual(response.json["Contacts"][0]["contactDate"], "2016-02-02")
        self.assertEqual(response.json["Contacts"][0]["initials"], "atp")
        self.assertEqual(response.json["Contacts"][0]["notes"], "notes")
        
    def test_get_contact(self):
        response = self.client.get("/api/contacts/1/")
        self.assertEqual(response.json["contactID"], 1)
        self.assertEqual(response.json["contactTypeLUTID"], 1)
        self.assertEqual(response.json["projectPatientID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["description"], "desc")
        self.assertEqual(response.json["contactDate"], "2016-02-02")
        self.assertEqual(response.json["initials"], "atp")
        self.assertEqual(response.json["notes"], "notes")
        
    def test_update_contact(self):
        response = self.client.put("/api/contacts/1/",data = {
            "contactTypeLUTID" : 2,
            "projectPatientID" : 2,
            "staffID" : 2,
            "informantID" : 2,
            "facilityID" : 2,
            "physicianID" : 2,
            "description" : "desc Updated",
            "contactDate" : "2016-02-03",
            "initials" : "atp Updated",
            "notes" : "notes Updated"
        })
        self.assertEqual(response.json["contactID"], 1)
        self.assertEqual(response.json["contactTypeLUTID"], 2)
        self.assertEqual(response.json["projectPatientID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["description"], "desc Updated")
        self.assertEqual(response.json["contactDate"], "2016-02-03")
        self.assertEqual(response.json["initials"], "atp Updated")
        self.assertEqual(response.json["notes"], "notes Updated")
        
    def test_delete_contact(self):
        response = self.client.delete("/api/contacts/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactID 1 deleted")  
        
class TestContactType(PopulatedDB):
    def test_get_contact_types(self):
        response = self.client.get("/api/contacttypes/")
        self.assertEqual(response.json["ContactTypes"][0]["contactTypeID"], 1)
        self.assertEqual(response.json["ContactTypes"][0]["contactDefinition"], "def")
        
    def test_get_contact_type(self):
        response = self.client.get("/api/contacttypes/1/")
        self.assertEqual(response.json["contactTypeID"], 1)
        self.assertEqual(response.json["contactDefinition"], "def")
        
    def test_update_contact_type(self):
        response = self.client.put("/api/contacttypes/1/",data = {
            "contactDefinition" : "def Updated",
        })
        self.assertEqual(response.json["contactTypeID"], 1)
        self.assertEqual(response.json["contactDefinition"], "def Updated")
        
    def test_delete_contact_type(self):
        response = self.client.delete("/api/contacttypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactTypeID 2 deleted")
        
class TestContactInfoSource(PopulatedDB):
    def test_get_contact_info_sourcees(self):
        response = self.client.get("/api/contactinfosources/")
        self.assertEqual(response.json["ContactInfoSources"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["ContactInfoSources"][0]["contactInfoSource"], "source")
        
    def test_get_contact_info_source(self):
        response = self.client.get("/api/contactinfosources/1/")
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["contactInfoSource"], "source")
        
    def test_update_contact_info_source(self):
        response = self.client.put("/api/contactinfosources/1/",data = {
            "contactInfoSource" : "source Updated",
        })
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["contactInfoSource"], "source Updated")
        
    def test_delete_contact_info_source(self):
        response = self.client.delete("/api/contactinfosources/2/")
        print(response.json)
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactInfoSourceID 2 deleted")
        
class TestContactInfoStatus(PopulatedDB):
    def test_get_contact_info_statuses(self):
        response = self.client.get("/api/contactinfostatuses/")
        self.assertEqual(response.json["ContactInfoStatuses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["ContactInfoStatuses"][0]["contactInfoStatus"], "status")
        
    def test_get_contact_info_status(self):
        response = self.client.get("/api/contactinfostatuses/1/")
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["contactInfoStatus"], "status")
        
    def test_update_contact_info_status(self):
        response = self.client.put("/api/contactinfostatuses/1/",data = {
            "contactInfoStatus" : "status Updated",
        })
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["contactInfoStatus"], "status Updated")
        
    def test_delete_contact_info_status(self):
        response = self.client.delete("/api/contactinfostatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactInfoStatusID 2 deleted")

class TestCTC(PopulatedDB):
    def test_get_ctcs(self):
        response = self.client.get("/api/ctcs/")
        self.assertEqual(response.json["CTCs"][0]["ctcID"], 1)
        self.assertEqual(response.json["CTCs"][0]["patientID"], 1)
        self.assertEqual(response.json["CTCs"][0]["dxDate"], "2016-02-02")
        self.assertEqual(response.json["CTCs"][0]["site"], 1)
        self.assertEqual(response.json["CTCs"][0]["histology"], "histology")
        self.assertEqual(response.json["CTCs"][0]["behavior"], "behavior")
        self.assertEqual(response.json["CTCs"][0]["ctcSequence"], "sequence")
        self.assertEqual(response.json["CTCs"][0]["stage"], "stage")
        self.assertEqual(response.json["CTCs"][0]["dxAge"], 1)
        self.assertEqual(response.json["CTCs"][0]["dxStreet1"], "street1")
        self.assertEqual(response.json["CTCs"][0]["dxStreet2"], "street2")
        self.assertEqual(response.json["CTCs"][0]["dxCity"], "city")
        self.assertEqual(response.json["CTCs"][0]["dxState"], "state")
        self.assertEqual(response.json["CTCs"][0]["dxZip"], 99999)
        self.assertEqual(response.json["CTCs"][0]["dxCounty"], "county")
        self.assertEqual(response.json["CTCs"][0]["dnc"], "dnc")
        self.assertEqual(response.json["CTCs"][0]["dncReason"], "dnc_reason")
        
    def test_get_ctc(self):
        response = self.client.get("/api/ctcs/1/")
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["dxDate"], "2016-02-02")
        self.assertEqual(response.json["site"], 1)
        self.assertEqual(response.json["histology"], "histology")
        self.assertEqual(response.json["behavior"], "behavior")
        self.assertEqual(response.json["ctcSequence"], "sequence")
        self.assertEqual(response.json["stage"], "stage")
        self.assertEqual(response.json["dxAge"], 1)
        self.assertEqual(response.json["dxStreet1"], "street1")
        self.assertEqual(response.json["dxStreet2"], "street2")
        self.assertEqual(response.json["dxCity"], "city")
        self.assertEqual(response.json["dxState"], "state")
        self.assertEqual(response.json["dxZip"], 99999)
        self.assertEqual(response.json["dxCounty"], "county")
        self.assertEqual(response.json["dnc"], "dnc")
        self.assertEqual(response.json["dncReason"], "dnc_reason")
        
    def test_update_ctc(self):
        response = self.client.put("/api/ctcs/1/",data = {
            "patientID" : 2,
            "dxDate" : "2016-02-03",
            "site" : 2,
            "histology" : "histology2",
            "behavior" : "behavior2",
            "ctcSequence" : "sequence2",
            "stage" : "stage2",
            "dxAge" : 2,
            "dxStreet1" : "street12",
            "dxStreet2" : "street22",
            "dxCity" : "city2",
            "dxState" : "state2",
            "dxZip" : 99991,
            "dxCounty" : "county2",
            "dnc" : "dnc2",
            "dncReason" : "dnc_reason2"
        })
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["dxDate"], "2016-02-03")
        self.assertEqual(response.json["site"], 2)
        self.assertEqual(response.json["histology"], "histology2")
        self.assertEqual(response.json["behavior"], "behavior2")
        self.assertEqual(response.json["ctcSequence"], "sequence2")
        self.assertEqual(response.json["stage"], "stage2")
        self.assertEqual(response.json["dxAge"], 2)
        self.assertEqual(response.json["dxStreet1"], "street12")
        self.assertEqual(response.json["dxStreet2"], "street22")
        self.assertEqual(response.json["dxCity"], "city2")
        self.assertEqual(response.json["dxState"], "state2")
        self.assertEqual(response.json["dxZip"], 99991)
        self.assertEqual(response.json["dxCounty"], "county2")
        self.assertEqual(response.json["dnc"], "dnc2")
        self.assertEqual(response.json["dncReason"], "dnc_reason2")
        
    def test_delete_ctc(self):
        response = self.client.delete("/api/ctcs/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "CtcID 2 deleted")

class TestCTCFacility(PopulatedDB):
    def test_get_ctc_facilities(self):
        response = self.client.get("/api/ctcfacilities/")
        self.assertEqual(response.json["CTCFacilities"][0]["CTCFacilityID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["ctcID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["facilityID"], 1)
        
    def test_get_ctc_facility(self):
        response = self.client.get("/api/ctcfacilities/1/")
        self.assertEqual(response.json["CTCFacilityID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        
    def test_update_ctc_facility(self):
        response = self.client.put("/api/ctcfacilities/1/",data = {
            "ctcID" : 2,
            "facilityID" : 2
        })
        self.assertEqual(response.json["CTCFacilityID"], 1)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        
    def test_delete_ctc_facility(self):
        response = self.client.delete("/api/ctcfacilities/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "CTCFacilityID 1 deleted")
             
class TestFacilityPhone(PopulatedDB):
    def test_get_facility_phones(self):
        response = self.client.get("/api/facilityphones/")
        self.assertEqual(response.json["FacilityPhones"][0]["facilityPhoneID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["facilityID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["clinicName"], "clinic")
        self.assertEqual(response.json["FacilityPhones"][0]["phoneType"], "cell")
        self.assertEqual(response.json["FacilityPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["FacilityPhones"][0]["phoneStatus"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["phoneSource"], "s1")
        self.assertEqual(response.json["FacilityPhones"][0]["phoneStatusDate"], "2016-02-02")
        
    def test_get_facility_phone(self):
        response = self.client.get("/api/facilityphones/1/")
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["clinicName"], "clinic")
        self.assertEqual(response.json["phoneType"], "cell")
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatus"], 1)
        self.assertEqual(response.json["phoneSource"], "s1")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        
    def test_update_facility_phone(self):
        response = self.client.put("/api/facilityphones/1/", data = {
            "contactInfoSourceID" : 2,
            "facilityID" : 2,
            "contactInfoStatusID" : 2,
            "facilityName" : "name Updated",
            "clinicName" : "clinic Updated",
            "phoneType" : "home",
            "phoneNumber" : "phone Updated",
            "phoneStatus" : 2,
            "phoneSource" : "s2",
            "phoneStatusDate" : "2016-02-03"
        })
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["clinicName"], "clinic Updated")
        self.assertEqual(response.json["phoneType"], "home")
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneStatus"], 2)
        self.assertEqual(response.json["phoneSource"], "s2")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")

    def test_delete_facility_phone(self):
        response = self.client.delete("/api/facilityphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityPhoneID 1 deleted")      

class TestFacility(PopulatedDB):
    def test_get_facilities(self):
        response = self.client.get("/api/facilities/")
        self.assertEqual(response.json["Facilities"][0]["facilityName"], "name")
        self.assertEqual(response.json["Facilities"][0]["contactFirstName"], "fname")
        self.assertEqual(response.json["Facilities"][0]["contactLastName"], "lname")
        self.assertEqual(response.json["Facilities"][0]["facilityStatus"], 1)
        self.assertEqual(response.json["Facilities"][0]["facilityStatusDate"], "2016-02-02")
        self.assertEqual(response.json["Facilities"][0]["contact2FirstName"], "fname")
        self.assertEqual(response.json["Facilities"][0]["contact2LastName"], "lname")

    def test_get_facility(self):
        response = self.client.get("/api/facilities/1/")
        self.assertEqual(response.json["facilityName"], "name")
        self.assertEqual(response.json["contactFirstName"], "fname")
        self.assertEqual(response.json["contactLastName"], "lname")
        self.assertEqual(response.json["facilityStatus"], 1)
        self.assertEqual(response.json["facilityStatusDate"], "2016-02-02")
        self.assertEqual(response.json["contact2FirstName"], "fname")
        self.assertEqual(response.json["contact2LastName"], "lname")
        
    def test_update_facility(self):
        response = self.client.put("/api/facilities/1/", data = {
            "facilityName" : "name2",
            "contactFirstName" : "fname2",
            "contactLastName" : "lname2",
            "facilityStatus" : 2,
            "facilityStatusDate" : "2016-02-03",
            "contact2FirstName" : "fname2",
            "contact2LastName" : "lname2"
        })
        self.assertEqual(response.json["facilityName"], "name2")
        self.assertEqual(response.json["contactFirstName"], "fname2")
        self.assertEqual(response.json["contactLastName"], "lname2")
        self.assertEqual(response.json["facilityStatus"], 2)
        self.assertEqual(response.json["facilityStatusDate"], "2016-02-03")
        self.assertEqual(response.json["contact2FirstName"], "fname2")
        self.assertEqual(response.json["contact2LastName"], "lname2")

    def test_delete_facility(self):
        response = self.client.delete("/api/facilities/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityID 2 deleted")

class TestFacilityAddress(PopulatedDB):
    def test_get_facility_addresses(self):
        response = self.client.get("/api/facilityaddresses/")
        self.assertEqual(response.json["FacilityAddresses"][0]["facilityAddressID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["facilityID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["street"], "street")
        self.assertEqual(response.json["FacilityAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["FacilityAddresses"][0]["city"], "city")
        self.assertEqual(response.json["FacilityAddresses"][0]["state"], "state")
        self.assertEqual(response.json["FacilityAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["FacilityAddresses"][0]["addressStatus"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["FacilityAddresses"][0]["addressStatusSource"], "s1")
        
    def test_get_facility_address(self):
        response = self.client.get("/api/facilityaddresses/1/")
        self.assertEqual(response.json["facilityAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["addressStatus"], 1)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["addressStatusSource"], "s1")
        
    def test_update_facility_address(self):
        response = self.client.put("/api/facilityaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "facilityID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "addressStatus" : 2,
            "addressStatusDate" : "2016-02-03",
            "addressStatusSource" : "s2"
        })
        self.assertEqual(response.json["facilityAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatus"], 2)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["addressStatusSource"], "s2")
        
    def test_delete_facility_address(self):
        response = self.client.delete("/api/facilityaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityAddressID 1 deleted")       
        
class TestFunding(PopulatedDB):
    def test_get_fundings(self):
        response = self.client.get("/api/fundings/")
        self.assertEqual(response.json["Fundings"][0]["fundingID"], 1)
        self.assertEqual(response.json["Fundings"][0]["grantStatusID"], 1)
        self.assertEqual(response.json["Fundings"][0]["projectID"], 1)
        self.assertEqual(response.json["Fundings"][0]["fundingSourceID"], 1)
        self.assertEqual(response.json["Fundings"][0]["primaryFundingSource"], "pfs")
        self.assertEqual(response.json["Fundings"][0]["secondaryFundingSource"], "sfs")
        self.assertEqual(response.json["Fundings"][0]["fundingNumber"], "number")
        self.assertEqual(response.json["Fundings"][0]["grantTitle"], "title")
        self.assertEqual(response.json["Fundings"][0]["dateStatus"], "2016-02-02")
        self.assertEqual(response.json["Fundings"][0]["grantPi"], 1)
        self.assertEqual(response.json["Fundings"][0]["primaryChartfield"], "pcf")
        self.assertEqual(response.json["Fundings"][0]["secondaryChartfield"], "scf")

    def test_get_funding(self):
        response = self.client.get("/api/fundings/1/")
        self.assertEqual(response.json["fundingID"], 1)
        self.assertEqual(response.json["grantStatusID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["fundingSourceID"], 1)
        self.assertEqual(response.json["primaryFundingSource"], "pfs")
        self.assertEqual(response.json["secondaryFundingSource"], "sfs")
        self.assertEqual(response.json["fundingNumber"], "number")
        self.assertEqual(response.json["grantTitle"], "title")
        self.assertEqual(response.json["dateStatus"], "2016-02-02")
        self.assertEqual(response.json["grantPi"], 1)
        self.assertEqual(response.json["primaryChartfield"], "pcf")
        self.assertEqual(response.json["secondaryChartfield"], "scf")
        
    def test_update_funding(self):
        response = self.client.put("/api/fundings/1/", data = {
            "fundingID": 1,
            "grantStatusID": 2,
            "projectID": 2,
            "fundingSourceID": 2,
            "primaryFundingSource": "pfs Updated",
            "secondaryFundingSource": "sfs Updated",
            "fundingNumber": "number Updated",
            "grantTitle": "title Updated",
            "dateStatus": "2016-02-03",
            "grantPi": 2,
            "primaryChartfield": "pcf Updated",
            "secondaryChartfield": "scf Updated"
        })
        self.assertEqual(response.json["fundingID"], 1)
        self.assertEqual(response.json["grantStatusID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["fundingSourceID"], 2)
        self.assertEqual(response.json["primaryFundingSource"], "pfs Updated")
        self.assertEqual(response.json["secondaryFundingSource"], "sfs Updated")
        self.assertEqual(response.json["fundingNumber"], "number Updated")
        self.assertEqual(response.json["grantTitle"], "title Updated")
        self.assertEqual(response.json["dateStatus"], "2016-02-03")
        self.assertEqual(response.json["grantPi"], 2)
        self.assertEqual(response.json["primaryChartfield"], "pcf Updated")
        self.assertEqual(response.json["secondaryChartfield"], "scf Updated")
        
    def test_delete_funding(self):
        response = self.client.delete("/api/fundings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingID 1 deleted")  
        
class TestFundingSource(PopulatedDB):
    def test_get_funding_sources(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json["FundingSources"][0]["fundingSourceID"], 1)
        self.assertEqual(response.json["FundingSources"][0]["fundingSource"], "source")

    def test_get_funding_source(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json["fundingSourceID"], 1)
        self.assertEqual(response.json["fundingSource"], "source")
        
    def test_update_funding_source(self):
        response = self.client.put("/api/fundingsources/1/", data = {
            "fundingSource" : "source2",
        })
        self.assertEqual(response.json["fundingSource"], "source2")
        
    def test_delete_funding_source(self):
        response = self.client.delete("/api/fundingsources/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingSourceID 2 deleted")
        
class TestGrantStatus(PopulatedDB):
    def test_get_grant_statuses(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json["GrantStatuses"][0]["grantStatusID"], 1)
        self.assertEqual(response.json["GrantStatuses"][0]["grantStatus"], "status")

    def test_get_grant_status(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json["grantStatusID"], 1)
        self.assertEqual(response.json["grantStatus"], "status")
        
    def test_update_grant_status(self):
        response = self.client.put("/api/grantstatuses/1/", data = {
            "grantStatus" : "status2"
        })
        self.assertEqual(response.json["grantStatus"], "status2")
        
    def test_delete_grant_status(self):
        response = self.client.delete("/api/grantstatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "GrantStatusID 2 deleted")

class TestHumanSubjectTraining(PopulatedDB):
    def test_get_human_subject_trainings(self):
        response = self.client.get("/api/humansubjecttrainings/")
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["trainingType"], "type")

    def test_get_human_subject_training(self):
        response = self.client.get("/api/humansubjecttrainings/1/")
        self.assertEqual(response.json["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["trainingType"], "type")
        
    def test_update_human_subject_training(self):
        response = self.client.put("/api/humansubjecttrainings/1/", data = {
            "trainingType" : "type Updated",
        })
        self.assertEqual(response.json["trainingType"], "type Updated")
        
    def test_delete_human_subject_training(self):
        response = self.client.delete("/api/humansubjecttrainings/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "HumanSubjectTrainingID 2 deleted")

class TestInformant(PopulatedDB):
    def test_get_informants(self):
        response = self.client.get("/api/informants/")
        self.assertEqual(response.json["Informants"][0]["informantID"], 1)
        self.assertEqual(response.json["Informants"][0]["patientID"], 1)
        self.assertEqual(response.json["Informants"][0]["firstName"], "fname")
        self.assertEqual(response.json["Informants"][0]["lastName"], "lname")
        self.assertEqual(response.json["Informants"][0]["middleName"], "middle_name")
        self.assertEqual(response.json["Informants"][0]["informantPrimary"], "informant_primary")
        self.assertEqual(response.json["Informants"][0]["informantRelationship"], "informant_relationship")
        self.assertEqual(response.json["Informants"][0]["notes"], "notes")
        
    def test_get_informant(self):
        response = self.client.get("/api/informants/1/")
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["middleName"], "middle_name")
        self.assertEqual(response.json["informantPrimary"], "informant_primary")
        self.assertEqual(response.json["informantRelationship"], "informant_relationship")
        self.assertEqual(response.json["notes"], "notes")
        
    def test_update_informant(self):
        response = self.client.put("/api/informants/1/", data = {
            "patientID" : 2,
            "firstName" : "fname Updated",
            "lastName" : "lname Updated",
            "middleName" : "middle_name Updated",
            "informantPrimary" : "informant_primary Updated",
            "informantRelationship" : "informant_relationship Updated",
            "notes" : "notes Updated"
        }) 
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["firstName"], "fname Updated")
        self.assertEqual(response.json["lastName"], "lname Updated")
        self.assertEqual(response.json["middleName"], "middle_name Updated")
        self.assertEqual(response.json["informantPrimary"], "informant_primary Updated")
        self.assertEqual(response.json["informantRelationship"], "informant_relationship Updated")
        self.assertEqual(response.json["notes"], "notes Updated")
        
    def test_delete_informant(self):
        response = self.client.delete("/api/informants/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantID 2 deleted")
        
class TestInformantAddress(PopulatedDB):
    def test_get_informant_addresses(self):
        response = self.client.get("/api/informantaddresses/")
        self.assertEqual(response.json["InformantAddresses"][0]["informantAddressID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["informantID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["street"], "street")
        self.assertEqual(response.json["InformantAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["InformantAddresses"][0]["city"], "city")
        self.assertEqual(response.json["InformantAddresses"][0]["state"], "state")
        self.assertEqual(response.json["InformantAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["InformantAddresses"][0]["addressStatus"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["InformantAddresses"][0]["addressStatusSource"], "s1")
        
    def test_get_informant_address(self):
        response = self.client.get("/api/informantaddresses/1/")
        self.assertEqual(response.json["informantAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["addressStatus"], 1)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["addressStatusSource"], "s1")
        
    def test_update_informant_address(self):
        response = self.client.put("/api/informantaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "informantID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "addressStatus" : 2,
            "addressStatusDate" : "2016-02-03",
            "addressStatusSource" : "s2"
        })
        self.assertEqual(response.json["informantAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatus"], 2)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["addressStatusSource"], "s2")
        
    def test_delete_informant_address(self):
        response = self.client.delete("/api/informantaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantAddressID 1 deleted")          
        
class TestInformantPhone(PopulatedDB):
    def test_get_informant_phones(self):
        response = self.client.get("/api/informantphones/")
        self.assertEqual(response.json["InformantPhones"][0]["informantPhoneID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["informantID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["InformantPhones"][0]["phoneStatus"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["phoneSource"], "s1")
        self.assertEqual(response.json["InformantPhones"][0]["phoneStatusDate"], "2016-02-02")
        
    def test_get_informant_phone(self):
        response = self.client.get("/api/informantphones/1/")
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatus"], 1)
        self.assertEqual(response.json["phoneSource"], "s1")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        
    def test_update_informant_phone(self):
        response = self.client.put("/api/informantphones/1/", data = {
            "contactInfoSourceID" : 2,
            "informantID" : 2,
            "contactInfoStatusID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneStatus" : 2,
            "phoneSource" : "s2",
            "phoneStatusDate" : "2016-02-03"
        })
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneStatus"], 2)
        self.assertEqual(response.json["phoneSource"], "s2")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        
    def test_delete_informant_phone(self):
        response = self.client.delete("/api/informantphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantPhoneID 1 deleted")  
        
class TestIRBHolder(PopulatedDB):
    def test_get_irb_holders(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json["irbHolders"][0]["holder"],"holder 1")
        self.assertEqual(response.json["irbHolders"][0]["holderDefinition"],"IRB 1")
        
    def test_get_irb_holder(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json["holder"],"holder 1")
        self.assertEqual(response.json["holderDefinition"],"IRB 1")
        
    def test_update_irb_holder(self):
        response = self.client.put("/api/irbholders/1/", data = {
            "holder" : "holder 1 Updated",
            "holderDefinition" : "IRB 1 Updated"
        })
        self.assertEqual(response.json["holder"],"holder 1 Updated")
        self.assertEqual(response.json["holderDefinition"],"IRB 1 Updated")
        
    def test_delete_irb_holder(self):
        response = self.client.delete("/api/irbholders/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "IrbHolderID 2 deleted")

class TestLog(PopulatedDB):
    def test_get_logs(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.json["Logs"][0]["logSubjectID"],1)
        self.assertEqual(response.json["Logs"][0]["projectID"],1)
        self.assertEqual(response.json["Logs"][0]["staffID"],1)
        self.assertEqual(response.json["Logs"][0]["phaseStatusID"],1)
        self.assertEqual(response.json["Logs"][0]["note"],"note")
        self.assertEqual(response.json["Logs"][0]["date"],"2016-02-02")
        
    def test_get_log(self):
        response = self.client.get("/api/logs/1/")
        self.assertEqual(response.json["logSubjectID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["phaseStatusID"],1)
        self.assertEqual(response.json["note"],"note")
        self.assertEqual(response.json["date"],"2016-02-02")
        
    def test_update_log(self):
        response = self.client.put("/api/logs/1/", data = {
            "logSubjectID" : 2,
            "projectID" : 2,
            "staffID" : 2,
            "phaseStatusID" : 2,
            "note" : "note Updated",
            "date" : "2016-02-03",
        })
        self.assertEqual(response.json["logSubjectID"],2)
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["staffID"],2)
        self.assertEqual(response.json["phaseStatusID"],2)
        self.assertEqual(response.json["note"],"note Updated")
        self.assertEqual(response.json["date"],"2016-02-03")
        
    def test_delete_log(self):
        response = self.client.delete("/api/logs/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogID 1 deleted")  
        
class TestLogSubject(PopulatedDB):
    def test_get_log_subjects(self):
        response = self.client.get("/api/logsubjects/")
        self.assertEqual(response.json["LogSubjects"][0]["logSubject"], "subject")
        
    def test_get_log_subject(self):
        response = self.client.get("/api/logsubjects/1/")
        self.assertEqual(response.json["logSubject"], "subject")
        
    def test_update_log_subject(self):
        response = self.client.put("/api/logsubjects/1/", data = {
            "logSubject" : "subject Updated",
        })
        self.assertEqual(response.json["logSubject"], "subject Updated")
        
    def test_delete_log_subject(self):
        response = self.client.delete("/api/logsubjects/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogSubjectID 2 deleted")
               
class TestPatient(PopulatedDB):
    def test_get_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json["Patients"][0]["patID"], "1")
        self.assertEqual(response.json["Patients"][0]["recordID"], 1)
        self.assertEqual(response.json["Patients"][0]["ucrDistID"], 1)
        self.assertEqual(response.json["Patients"][0]["UPDBID"], 1)
        self.assertEqual(response.json["Patients"][0]["firstName"], "fname")
        self.assertEqual(response.json["Patients"][0]["lastName"], "lname")
        self.assertEqual(response.json["Patients"][0]["maidenName"], "maiden_name")
        self.assertEqual(response.json["Patients"][0]["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["Patients"][0]["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["Patients"][0]["aliasMiddleName"], "alias_middle")
        self.assertEqual(response.json["Patients"][0]["dob"], "2016-02-02")
        self.assertEqual(response.json["Patients"][0]["SSN"], 999999999)
        self.assertEqual(response.json["Patients"][0]["sex"], "male")
        self.assertEqual(response.json["Patients"][0]["race"], "white")
        self.assertEqual(response.json["Patients"][0]["ethnicity"], "hispanic")
        self.assertEqual(response.json["Patients"][0]["vitalStatus"], "v1")
        
    def test_get_patient(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json["patID"], "1")
        self.assertEqual(response.json["recordID"], 1)
        self.assertEqual(response.json["ucrDistID"], 1)
        self.assertEqual(response.json["UPDBID"], 1)
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["maidenName"], "maiden_name")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle")
        self.assertEqual(response.json["dob"], "2016-02-02")
        self.assertEqual(response.json["SSN"], 999999999)
        self.assertEqual(response.json["sex"], "male")
        self.assertEqual(response.json["race"], "white")
        self.assertEqual(response.json["ethnicity"], "hispanic")
        self.assertEqual(response.json["vitalStatus"], "v1")
        
    def test_update_patient(self):
        response = self.client.put("/api/patients/1/", data = {
            "patID" : "2",
            "recordID" : 2,
            "ucrDistID" : 2,
            "UPDBID" : 2,
            "firstName" : "fname Updated",
            "lastName" : "lname Updated",
            "middleName" : "mname Updated",
            "maidenName" : "maiden_name Updated",
            "aliasFirstName" : "alias_fname Updated",
            "aliasLastName" : "alias_lname Updated",
            "aliasMiddleName" : "alias_middle Updated",
            "dob" : "2016-02-03",
            "SSN" : "999999990",
            "sex" : "female",
            "race" : "black",
            "ethnicity" : "non-hispanic",
            "vitalStatus" : "v2"
        })
        self.assertEqual(response.json["patID"], "2")
        self.assertEqual(response.json["recordID"], 2)
        self.assertEqual(response.json["ucrDistID"], 2)
        self.assertEqual(response.json["UPDBID"], 2)
        self.assertEqual(response.json["firstName"], "fname Updated")
        self.assertEqual(response.json["lastName"], "lname Updated")
        self.assertEqual(response.json["maidenName"], "maiden_name Updated")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname Updated")
        self.assertEqual(response.json["aliasLastName"], "alias_lname Updated")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle Updated")
        self.assertEqual(response.json["dob"], "2016-02-03")
        self.assertEqual(response.json["SSN"], 999999990)
        self.assertEqual(response.json["sex"], "female")
        self.assertEqual(response.json["race"], "black")
        self.assertEqual(response.json["ethnicity"], "non-hispanic")
        self.assertEqual(response.json["vitalStatus"], "v2")
        
    def test_delete_patient(self):
        response = self.client.delete("/api/patients/2/")
        print(response.json)
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientID 2 deleted")

class TestPatientAddress(PopulatedDB):
    def test_get_patient_addresses(self):
        response = self.client.get("/api/patientaddresses/")
        self.assertEqual(response.json["PatientAddresses"][0]["patAddressID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["patientID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["street"], "street")
        self.assertEqual(response.json["PatientAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["PatientAddresses"][0]["city"], "city")
        self.assertEqual(response.json["PatientAddresses"][0]["state"], "state")
        self.assertEqual(response.json["PatientAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["PatientAddresses"][0]["addressStatus"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PatientAddresses"][0]["addressStatusSource"], "s1")
        
    def test_get_patient_address(self):
        response = self.client.get("/api/patientaddresses/1/")
        self.assertEqual(response.json["patAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["addressStatus"], 1)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["addressStatusSource"], "s1")
        
    def test_update_patient_address(self):
        response = self.client.put("/api/patientaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "patientID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "addressStatus" : 2,
            "addressStatusDate" : "2016-02-03",
            "addressStatusSource" : "s2"
        })
        self.assertEqual(response.json["patAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatus"], 2)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["addressStatusSource"], "s2")
        
    def test_delete_patient_address(self):
        response = self.client.delete("/api/patientaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatAddressID 1 deleted")       

class TestPatientEmail(PopulatedDB):
    def test_get_patient_emails(self):
        response = self.client.get("/api/patientemails/")
        self.assertEqual(response.json["PatientEmails"][0]["emailID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["patientID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["email"], "email")
        self.assertEqual(response.json["PatientEmails"][0]["emailStatus"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["emailSource"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["emailStatusDate"], "2016-02-02")
        
    def test_get_patient_email(self):
        response = self.client.get("/api/patientemails/1/")
        self.assertEqual(response.json["emailID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["email"], "email")
        self.assertEqual(response.json["emailStatus"], 1)
        self.assertEqual(response.json["emailSource"], 1)
        self.assertEqual(response.json["emailStatusDate"], "2016-02-02")
        
    def test_update_patient_email(self):
        response = self.client.put("/api/patientemails/1/", data = {
            "contactInfoSourceID" : 2,
            "patientID" : 2,
            "contactInfoStatusID" : 2,
            "email" : "email Updated",
            "emailStatus" : 2,
            "emailSource" : 2,
            "emailStatusDate" : "2016-02-03"
        })
        self.assertEqual(response.json["emailID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["email"], "email Updated")
        self.assertEqual(response.json["emailStatus"], 2)
        self.assertEqual(response.json["emailSource"], 2)
        self.assertEqual(response.json["emailStatusDate"], "2016-02-03")
        
    def test_delete_patient_email(self):
        response = self.client.delete("/api/patientemails/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "EmailID 1 deleted")           

class TestPatientPhone(PopulatedDB):
    def test_get_patient_phones(self):
        response = self.client.get("/api/patientphones/")
        self.assertEqual(response.json["PatientPhones"][0]["patPhoneID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["patientID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["PatientPhones"][0]["phoneStatus"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["phoneSource"], "s1")
        self.assertEqual(response.json["PatientPhones"][0]["phoneStatusDate"], "2016-02-02")
        
    def test_get_patient_phone(self):
        response = self.client.get("/api/patientphones/1/")
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatus"], 1)
        self.assertEqual(response.json["phoneSource"], "s1")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        
    def test_update_patient_phone(self):
        response = self.client.put("/api/patientphones/1/", data = {
            "contactInfoSourceID" : 2,
            "patientID" : 2,
            "contactInfoStatusID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneStatus" : 2,
            "phoneSource" : "s2",
            "phoneStatusDate" : "2016-02-03"
        })
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneStatus"], 2)
        self.assertEqual(response.json["phoneSource"], "s2")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        
    def test_delete_patient_phone(self):
        response = self.client.delete("/api/patientphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatPhoneID 1 deleted")      

class TestPatientProjectStatus(PopulatedDB):
    def test_get_patient_project_statuses(self):
        response = self.client.get("/api/patientprojectstatuses/")
        self.assertEqual(response.json["PatientProjectStatuses"][0]["patientProjectStatusID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["projectPatientID"], 1)
        
    def test_get_patient_project_status(self):
        response = self.client.get("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json["patientProjectStatusID"], 1)
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["projectPatientID"], 1)
        
    def test_update_patient_project_status(self):
        response = self.client.put("/api/patientprojectstatuses/1/", data = {
            "patientProjectStatusTypeID" : 2,
            "projectPatientID" : 2
        })
        self.assertEqual(response.json["patientProjectStatusID"], 1)
        self.assertEqual(response.json["patientProjectStatusTypeID"], 2)
        self.assertEqual(response.json["projectPatientID"], 2)
        
    def test_delete_patient_project_status(self):
        response = self.client.delete("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientProjectStatusID 1 deleted")   

class TestPatientProjectStatusLUT(PopulatedDB):
    def test_get_patient_project_status_types(self):
        response = self.client.get("/api/patientprojectstatustypes/")
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["statusDescription"], "desc")

    def test_get_patient_project_status_type(self):
        response = self.client.get("/api/patientprojectstatustypes/1/")
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["statusDescription"], "desc")

    def test_update_patient_project_status_type(self):
        response = self.client.put("/api/patientprojectstatustypes/1/", data = {
            "statusDescription" : "desc Updated"
        })
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["statusDescription"], "desc Updated")

    def test_delete_patient_project_status_type(self):
        response = self.client.delete("/api/patientprojectstatustypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientProjectStatusTypeID 2 deleted")
        
class TestPhaseStatus(PopulatedDB):
    def test_get_phase_statuses(self):
        response = self.client.get("/api/phasestatuses/")
        self.assertEqual(response.json["PhaseStatuses"][0]["phaseStatus"], "status")
        self.assertEqual(response.json["PhaseStatuses"][0]["phaseDescription"], "desc")
        
    def test_get_phase_status(self):
        response = self.client.get("/api/phasestatuses/1/")
        self.assertEqual(response.json["phaseStatus"], "status")
        self.assertEqual(response.json["phaseDescription"], "desc")
        
    def test_update_phase_status(self):
        response = self.client.put("/api/phasestatuses/1/", data = {
            "phaseStatus" : "status Updated",
            "phaseDescription": "desc Updated"
        })
        self.assertEqual(response.json["phaseStatus"], "status Updated")
        self.assertEqual(response.json["phaseDescription"], "desc Updated")
        
    def test_delete_phase_status(self):
        response = self.client.delete("/api/phasestatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogPhaseID 2 deleted")

class TestPhysician(PopulatedDB):
    def test_get_physicians(self):
        response = self.client.get("/api/physicians/")
        self.assertEqual(response.json["Physicians"][0]["firstName"], "fname")
        self.assertEqual(response.json["Physicians"][0]["lastName"], "lname")
        self.assertEqual(response.json["Physicians"][0]["middleName"], "middle_name")
        self.assertEqual(response.json["Physicians"][0]["credentials"], "credentials")
        self.assertEqual(response.json["Physicians"][0]["specialty"], "specialty")
        self.assertEqual(response.json["Physicians"][0]["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["Physicians"][0]["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["Physicians"][0]["aliasMiddleName"], "alias_middle_name")
        self.assertEqual(response.json["Physicians"][0]["physicianStatus"], 1)
        self.assertEqual(response.json["Physicians"][0]["physicianStatusDate"], "2016-02-02")
        self.assertEqual(response.json["Physicians"][0]["email"], "email")
        
    def test_get_physician(self):
        response = self.client.get("/api/physicians/1/")
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["middleName"], "middle_name")
        self.assertEqual(response.json["credentials"], "credentials")
        self.assertEqual(response.json["specialty"], "specialty")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle_name")
        self.assertEqual(response.json["physicianStatus"], 1)
        self.assertEqual(response.json["physicianStatusDate"], "2016-02-02")
        self.assertEqual(response.json["email"], "email")
        
    def test_update_physician(self):
        response = self.client.put("/api/physicians/1/", data = {
            "firstName" : "fname2",
            "lastName" : "lname2",
            "middleName" : "middle_name2",
            "credentials" : "credentials2",
            "specialty" : "specialty2",
            "aliasFirstName" : "alias_fname2",
            "aliasLastName" : "alias_lname2",
            "aliasMiddleName" : "alias_middle_name2",
            "physicianStatus" : 2,
            "physicianStatusDate" : "2016-02-03",
            "email" : "email2"
        })
        self.assertEqual(response.json["firstName"], "fname2")
        self.assertEqual(response.json["lastName"], "lname2")
        self.assertEqual(response.json["middleName"], "middle_name2")
        self.assertEqual(response.json["credentials"], "credentials2")
        self.assertEqual(response.json["specialty"], "specialty2")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname2")
        self.assertEqual(response.json["aliasLastName"], "alias_lname2")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle_name2")
        self.assertEqual(response.json["physicianStatus"], 2)
        self.assertEqual(response.json["physicianStatusDate"], "2016-02-03")
        self.assertEqual(response.json["email"], "email2")
        
    def test_delete_physician(self):
        response = self.client.delete("/api/physicians/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianID 2 deleted")

class TestPhysicianAddress(PopulatedDB):
    def test_get_physician_addresses(self):
        response = self.client.get("/api/physicianaddresses/")
        self.assertEqual(response.json["PhysicianAddresses"][0]["physicianAddressID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["street"], "street")
        self.assertEqual(response.json["PhysicianAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["PhysicianAddresses"][0]["city"], "city")
        self.assertEqual(response.json["PhysicianAddresses"][0]["state"], "state")
        self.assertEqual(response.json["PhysicianAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["PhysicianAddresses"][0]["addressStatus"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PhysicianAddresses"][0]["addressStatusSource"], "s1")
        
    def test_get_physician_address(self):
        response = self.client.get("/api/physicianaddresses/1/")
        self.assertEqual(response.json["physicianAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["addressStatus"], 1)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["addressStatusSource"], "s1")
        
    def test_update_physician_address(self):
        response = self.client.put("/api/physicianaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "physicianID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "addressStatus" : 2,
            "addressStatusDate" : "2016-02-03",
            "addressStatusSource" : "s2"
        })
        self.assertEqual(response.json["physicianAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatus"], 2)
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["addressStatusSource"], "s2")

    def test_delete_physician_address(self):
        response = self.client.delete("/api/physicianaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianAddressID 1 deleted")       

class TestPhysicianFacility(PopulatedDB):
    def test_get_physician_facilities(self):
        response = self.client.get("/api/physicianfacilities/")
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["facilityID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityStatus"], "s1")
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityStatusDate"], "2016-02-02")
        
    def test_get_physician_facility(self):
        response = self.client.get("/api/physicianfacilities/1/")
        self.assertEqual(response.json["physFacilityID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["physFacilityStatus"], "s1")
        self.assertEqual(response.json["physFacilityStatusDate"], "2016-02-02")
        
    def test_update_physician_facility(self):
        response = self.client.put("/api/physicianfacilities/1/", data = {
            "facilityID" : 2,
            "physicianID" : 2,
            "physFacilityStatus" : 2,
            "physFacilityStatusDate" : "2016-02-03"
        })
        self.assertEqual(response.json["physFacilityID"], 1)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["physFacilityStatus"], 2)
        self.assertEqual(response.json["physFacilityStatusDate"], "2016-02-03")
        
    def test_delete_physician_facility(self):
        response = self.client.delete("/api/physicianfacilities/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysFacilityID 1 deleted")      
        
class TestPhysicianPhone(PopulatedDB):
    def test_get_physician_phone(self):
        response = self.client.get("/api/physicianphones/")
        self.assertEqual(response.json["PhysicianPhones"][0]["physicianPhoneID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneType"], "phone_type")
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneStatus"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneSource"], "s1")
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneStatusDate"], "2016-02-02")
        
    def test_get_physician_phone(self):
        response = self.client.get("/api/physicianphones/1/")
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneType"], "phone_type")
        self.assertEqual(response.json["phoneStatus"], 1)
        self.assertEqual(response.json["phoneSource"], "s1")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        
    def test_update_physician_phone(self):
        response = self.client.put("/api/physicianphones/1/", data = {
            "contactInfoSourceID" : 2,
            "physicianID" : 2,
            "contactInfoStatusID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneType": "phone_type Updated",
            "phoneStatus" : 2,
            "phoneSource" : "s2",
            "phoneStatusDate" : "2016-02-03"
        })
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneType"], "phone_type Updated")
        self.assertEqual(response.json["phoneStatus"], 2)
        self.assertEqual(response.json["phoneSource"], "s2")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        
    def test_delete_physician_phone(self):
        response = self.client.delete("/api/physicianphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianPhoneID 1 deleted")      
        
class TestPhysicianToCTC(PopulatedDB):
    def test_get_physician_to_ctcs(self):
        response = self.client.get("/api/physiciantoctcs/")
        self.assertEqual(response.json["PhysicianToCTCs"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianToCTCs"][0]["ctcID"], 1)
        
    def test_get_physician_to_ctc(self):
        response = self.client.get("/api/physiciantoctcs/1/")
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        
    def test_update_physician_to_ctc(self):
        response = self.client.put("/api/physiciantoctcs/1/", data = {
            "physicianID" : 2,
            "ctcID": 2
        })
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        
    def test_delete_physician_to_ctc(self):
        response = self.client.delete("/api/physiciantoctcs/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianCTCID 1 deleted")       

class TestPreApplication(PopulatedDB):
    def test_get_pre_applications(self):
        response = self.client.get("/api/preapplications/")
        self.assertEqual(response.json["PreApplications"][0]["projectID"], 1)
        self.assertEqual(response.json["PreApplications"][0]["piFirstName"], "pi_fname")
        self.assertEqual(response.json["PreApplications"][0]["piLastName"], "pi_lname")
        self.assertEqual(response.json["PreApplications"][0]["piPhone"], "pi_phone")
        self.assertEqual(response.json["PreApplications"][0]["piEmail"], "pi_email")
        self.assertEqual(response.json["PreApplications"][0]["contactFirstName"], "contact_fname")
        self.assertEqual(response.json["PreApplications"][0]["contactLastName"], "contact_lname")
        self.assertEqual(response.json["PreApplications"][0]["contactPhone"], "contact_phone")
        self.assertEqual(response.json["PreApplications"][0]["contactEmail"], "contact_email")
        self.assertEqual(response.json["PreApplications"][0]["institution"], "institution")
        self.assertEqual(response.json["PreApplications"][0]["institution2"], "institution2")        
        self.assertEqual(response.json["PreApplications"][0]["uid"], "uid")
        self.assertEqual(response.json["PreApplications"][0]["udoh"], 1)
        self.assertEqual(response.json["PreApplications"][0]["projectTitle"], "project_title")
        self.assertEqual(response.json["PreApplications"][0]["purpose"], "purpose")
        self.assertEqual(response.json["PreApplications"][0]["irb0"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb1"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb2"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb3"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb4"], True)
        self.assertEqual(response.json["PreApplications"][0]["otherIrb"], "other_irb")
        self.assertEqual(response.json["PreApplications"][0]["updb"], True)
        self.assertEqual(response.json["PreApplications"][0]["ptContact"], True)
        self.assertEqual(response.json["PreApplications"][0]["startDate"], "2016-02-02")
        self.assertEqual(response.json["PreApplications"][0]["link"], True)
        self.assertEqual(response.json["PreApplications"][0]["deliveryDate"], "2016-02-02")
        self.assertEqual(response.json["PreApplications"][0]["description"], "description")
        
    def test_get_pre_application(self):
        response = self.client.get("/api/preapplications/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["piFirstName"], "pi_fname")
        self.assertEqual(response.json["piLastName"], "pi_lname")
        self.assertEqual(response.json["piPhone"], "pi_phone")
        self.assertEqual(response.json["piEmail"], "pi_email")
        self.assertEqual(response.json["contactFirstName"], "contact_fname")
        self.assertEqual(response.json["contactLastName"], "contact_lname")
        self.assertEqual(response.json["contactPhone"], "contact_phone")
        self.assertEqual(response.json["contactEmail"], "contact_email")
        self.assertEqual(response.json["institution"], "institution")
        self.assertEqual(response.json["institution2"], "institution2")
        self.assertEqual(response.json["uid"], "uid")
        self.assertEqual(response.json["udoh"], 1)
        self.assertEqual(response.json["projectTitle"], "project_title")
        self.assertEqual(response.json["purpose"], "purpose")
        self.assertEqual(response.json["irb0"], True)
        self.assertEqual(response.json["irb1"], True)
        self.assertEqual(response.json["irb2"], True)
        self.assertEqual(response.json["irb3"], True)
        self.assertEqual(response.json["irb4"], True)
        self.assertEqual(response.json["otherIrb"], "other_irb")
        self.assertEqual(response.json["updb"], True)
        self.assertEqual(response.json["ptContact"], True)
        self.assertEqual(response.json["startDate"], "2016-02-02")
        self.assertEqual(response.json["link"], True)
        self.assertEqual(response.json["deliveryDate"], "2016-02-02")
        self.assertEqual(response.json["description"], "description")
        
    def test_update_pre_application(self):
        response = self.client.put("/api/preapplications/1/", data = {
            "projectID" : 2,
            "piFirstName" : "pi_fname2",
            "piLastName" : "pi_lname2",
            "piEmail" : "pi_email2",
            "piPhone" : "pi_phone2",
            "contactFirstName" : "contact_fname2",
            "contactLastName" : "contact_lname2",
            "contactPhone" : "contact_phone2",
            "contactEmail" : "contact_email2",
            "institution" : "institution2",
            "institution2" : "institution22",
            "uid" : "uid2",
            "udoh" : 2,
            "projectTitle" : "project_title2",
            "purpose" : "purpose2",
            "irb0" : False,
            "irb1" : False,
            "irb2" : False,
            "irb3" : False,
            "irb4" : False,
            "otherIrb" : "other_irb2",
            "updb" : False,
            "ptContact" : False,
            "startDate" : "2016-02-03",
            "link" : False,
            "deliveryDate" : "2016-02-03",
            "description" : "description2"
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["piFirstName"], "pi_fname2")
        self.assertEqual(response.json["piLastName"], "pi_lname2")
        self.assertEqual(response.json["piPhone"], "pi_phone2")
        self.assertEqual(response.json["piEmail"], "pi_email2")
        self.assertEqual(response.json["contactFirstName"], "contact_fname2")
        self.assertEqual(response.json["contactLastName"], "contact_lname2")
        self.assertEqual(response.json["contactPhone"], "contact_phone2")
        self.assertEqual(response.json["contactEmail"], "contact_email2")
        self.assertEqual(response.json["institution"], "institution2")
        self.assertEqual(response.json["institution2"], "institution22")        
        self.assertEqual(response.json["uid"], "uid2")
        self.assertEqual(response.json["udoh"], 2)
        self.assertEqual(response.json["projectTitle"], "project_title2")
        self.assertEqual(response.json["purpose"], "purpose2")
        self.assertEqual(response.json["irb0"], False)
        self.assertEqual(response.json["irb1"], False)
        self.assertEqual(response.json["irb2"], False)
        self.assertEqual(response.json["irb3"], False)
        self.assertEqual(response.json["irb4"], False)
        self.assertEqual(response.json["otherIrb"], "other_irb2")
        self.assertEqual(response.json["updb"], False)
        self.assertEqual(response.json["ptContact"], False)
        self.assertEqual(response.json["startDate"], "2016-02-03")
        self.assertEqual(response.json["link"], False)
        self.assertEqual(response.json["deliveryDate"], "2016-02-03")
        self.assertEqual(response.json["description"], "description2")
        
    def test_delete_pre_application(self):
        response = self.client.delete("/api/preapplications/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PreApplicationID 1 deleted")    
        
class TestProject(PopulatedDB):

    # test getting list of projects
    def test_get_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.json["projects"][0]["projectID"],1)
        self.assertEqual(response.json["projects"][0]["projectTypeID"],1)
        self.assertEqual(response.json["projects"][0]["irbHolderID"],1)
        self.assertEqual(response.json["projects"][0]["projectName"],"Test Project")
        self.assertEqual(response.json["projects"][0]["shortTitle"],"Test Project")
        self.assertEqual(response.json["projects"][0]["projectSummary"],"Summary")
        self.assertEqual(response.json["projects"][0]["sop"],"sop")
        self.assertEqual(response.json["projects"][0]["ucrProposal"],"ucr_proposal")
        self.assertEqual(response.json["projects"][0]["budgetDoc"],"budget_doc")
        self.assertEqual(response.json["projects"][0]["ucrFee"],"no")
        self.assertEqual(response.json["projects"][0]["ucrNoFee"],"yes")
        self.assertEqual(response.json["projects"][0]["budgetEndDate"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["previousShortTitle"],"t short")
        self.assertEqual(response.json["projects"][0]["dateAdded"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["finalRecruitmentReport"],"report")
    # Test getting single project
    def test_get_project(self):
        response = self.client.get("/api/projects/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectTypeID"],1)
        self.assertEqual(response.json["irbHolderID"],1)
        self.assertEqual(response.json["projectName"],"Test Project")
        self.assertEqual(response.json["shortTitle"],"Test Project")
        self.assertEqual(response.json["projectSummary"],"Summary")
        self.assertEqual(response.json["sop"],"sop")
        self.assertEqual(response.json["ucrProposal"],"ucr_proposal")
        self.assertEqual(response.json["budgetDoc"],"budget_doc")
        self.assertEqual(response.json["ucrFee"],"no")
        self.assertEqual(response.json["ucrNoFee"],"yes")
        self.assertEqual(response.json["budgetEndDate"],"2016-02-02")
        self.assertEqual(response.json["previousShortTitle"],"t short")
        self.assertEqual(response.json["dateAdded"],"2016-02-02")
        self.assertEqual(response.json["finalRecruitmentReport"],"report")

    # Test update project
    def test_update_project(self):
        response = self.client.put("/api/projects/1/",data = {
            "projectTypeID" : 2,
            "irbHolderID" : 2,
            "projectName" : "Test Project Update",
            "shortTitle" : "Test Project Update",
            "projectSummary" : "Summary Update",
            "sop":"sop Update",
            "ucrProposal":"ucr_proposal Update",
            "budgetDoc" : "budget_doc Update",
            "ucrFee" : "no Update",
            "ucrNoFee" : "yes Update",
            "budgetEndDate" : "2016-02-03",
            "previousShortTitle" : "t short Update",
            "dateAdded" : "2016-02-03",
            "finalRecruitmentReport" : "report Update"
        })
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectTypeID"],2)
        self.assertEqual(response.json["irbHolderID"],2)
        self.assertEqual(response.json["projectName"],"Test Project Update")
        self.assertEqual(response.json["shortTitle"],"Test Project Update")
        self.assertEqual(response.json["projectSummary"],"Summary Update")
        self.assertEqual(response.json["sop"],"sop Update")
        self.assertEqual(response.json["ucrProposal"],"ucr_proposal Update")
        self.assertEqual(response.json["budgetDoc"],"budget_doc Update")
        self.assertEqual(response.json["ucrFee"],"no Update")
        self.assertEqual(response.json["ucrNoFee"],"yes Update")
        self.assertEqual(response.json["budgetEndDate"],"2016-02-03")
        self.assertEqual(response.json["previousShortTitle"],"t short Update")
        self.assertEqual(response.json["dateAdded"],"2016-02-03")
        self.assertEqual(response.json["finalRecruitmentReport"],"report Update")
        
     # Test deletetion of project
    def test_delete_project(self):
        response = self.client.delete("/api/projects/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectID 2 deleted")

class TestProjectPatient(PopulatedDB):
    def test_get_project_statuses(self):
        response = self.client.get("/api/projectpatients/")
        self.assertEqual(response.json["ProjectPatients"][0]["participantID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["ctcID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["currentAge"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["batch"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["siteGrp"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["finalCode"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["finalCodeDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["enrollmentDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["dateCoordSigned"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["importDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["finalCodeStaff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["enrollmentStaff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["dateCoordSignedStaff"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractStatus"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstractStatusDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractStatusStaff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["sentToAbstractorDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["sentToAbstractorStaff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstractedDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractorInitials"], "atp")
        self.assertEqual(response.json["ProjectPatients"][0]["researcherDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["researcherStaff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["consentLink"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["tracingStatus"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseSigned"], True)
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseLink"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseStaff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["surveyToResearcher"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["surveyToResearcherStaff"], 1)
        
    def test_get_project_patient(self):
        response = self.client.get("/api/projectpatients/1/")
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["currentAge"], 1)
        self.assertEqual(response.json["batch"], 1)
        self.assertEqual(response.json["siteGrp"], 1)
        self.assertEqual(response.json["finalCode"], 1)
        self.assertEqual(response.json["finalCodeDate"], "2016-02-02")
        self.assertEqual(response.json["enrollmentDate"], "2016-02-02")
        self.assertEqual(response.json["dateCoordSigned"], "2016-02-02")
        self.assertEqual(response.json["importDate"], "2016-02-02")
        self.assertEqual(response.json["finalCodeStaff"], 1)
        self.assertEqual(response.json["enrollmentStaff"], 1)
        self.assertEqual(response.json["dateCoordSignedStaff"], "2016-02-02")
        self.assertEqual(response.json["abstractStatus"], 1)
        self.assertEqual(response.json["abstractStatusDate"], "2016-02-02")
        self.assertEqual(response.json["abstractStatusStaff"], 1)
        self.assertEqual(response.json["sentToAbstractorDate"], "2016-02-02")
        self.assertEqual(response.json["sentToAbstractorStaff"], 1)
        self.assertEqual(response.json["abstractedDate"], "2016-02-02")
        self.assertEqual(response.json["abstractorInitials"], "atp")
        self.assertEqual(response.json["researcherDate"], "2016-02-02")
        self.assertEqual(response.json["researcherStaff"], 1)
        self.assertEqual(response.json["consentLink"], "link")
        self.assertEqual(response.json["tracingStatus"], 1)
        self.assertEqual(response.json["medRecordReleaseSigned"], True)
        self.assertEqual(response.json["medRecordReleaseLink"], "link")
        self.assertEqual(response.json["medRecordReleaseStaff"], 1)
        self.assertEqual(response.json["medRecordReleaseDate"], "2016-02-02")
        self.assertEqual(response.json["surveyToResearcher"], "2016-02-02")
        self.assertEqual(response.json["surveyToResearcherStaff"], 1)
        
    def test_update_project_patient(self):
        response = self.client.put("/api/projectpatients/1/", data = {
            "projectID" : 2,
            "staffID" : 2,
            "ctcID" : 2,
            "currentAge" : 2,
            "batch"  : 2,
            "siteGrp" : 2,
            "finalCode" : 2,
            "finalCodeDate" : "2016-02-03",
            "enrollmentDate" : "2016-02-03",
            "dateCoordSigned" : "2016-02-03",
            "importDate" : "2016-02-03",
            "finalCodeStaff" : 2,
            "enrollmentStaff" : 2,
            "dateCoordSignedStaff"  : "2016-02-03",
            "abstractStatus" : 2,
            "abstractStatusDate" : "2016-02-03",
            "abstractStatusStaff" : 2,
            "sentToAbstractorDate"  : "2016-02-03",
            "sentToAbstractorStaff" : 2,
            "abstractedDate" : "2016-02-03",
            "abstractorInitials" : "atp Updated",
            "researcherDate" : "2016-02-03",
            "researcherStaff" : 2,
            "consentLink" : "link Updated",
            "tracingStatus" : 2,
            "medRecordReleaseSigned" : False,
            "medRecordReleaseLink" : "link Updated",
            "medRecordReleaseStaff" : 2,
            "medRecordReleaseDate"  : "2016-02-03",
            "surveyToResearcher"  : "2016-02-03",
            "surveyToResearcherStaff" : 2
        })
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["currentAge"], 2)
        self.assertEqual(response.json["batch"], 2)
        self.assertEqual(response.json["siteGrp"], 2)
        self.assertEqual(response.json["finalCode"], 2)
        self.assertEqual(response.json["finalCodeDate"], "2016-02-03")
        self.assertEqual(response.json["enrollmentDate"], "2016-02-03")
        self.assertEqual(response.json["dateCoordSigned"], "2016-02-03")
        self.assertEqual(response.json["importDate"], "2016-02-03")
        self.assertEqual(response.json["finalCodeStaff"], 2)
        self.assertEqual(response.json["enrollmentStaff"], 2)
        self.assertEqual(response.json["dateCoordSignedStaff"], "2016-02-03")
        self.assertEqual(response.json["abstractStatus"], 2)
        self.assertEqual(response.json["abstractStatusDate"], "2016-02-03")
        self.assertEqual(response.json["abstractStatusStaff"], 2)
        self.assertEqual(response.json["sentToAbstractorDate"], "2016-02-03")
        self.assertEqual(response.json["sentToAbstractorStaff"], 2)
        self.assertEqual(response.json["abstractedDate"], "2016-02-03")
        self.assertEqual(response.json["abstractorInitials"], "atp Updated")
        self.assertEqual(response.json["researcherDate"], "2016-02-03")
        self.assertEqual(response.json["researcherStaff"], 2)
        self.assertEqual(response.json["consentLink"], "link Updated")
        self.assertEqual(response.json["tracingStatus"], 2)
        self.assertEqual(response.json["medRecordReleaseSigned"], False)
        self.assertEqual(response.json["medRecordReleaseLink"], "link Updated")
        self.assertEqual(response.json["medRecordReleaseStaff"], 2)
        self.assertEqual(response.json["medRecordReleaseDate"], "2016-02-03")
        self.assertEqual(response.json["surveyToResearcher"], "2016-02-03")
        self.assertEqual(response.json["surveyToResearcherStaff"], 2)
        
    def test_delete_project_patient(self):
        response = self.client.delete("/api/projectpatients/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ParticipantID 2 deleted")

class TestProjectStaff(PopulatedDB):
    def test_get_staffs(self):
        response = self.client.get("/api/projectstaff/")
        self.assertEqual(response.json["ProjectStaff"][0]["staffRoleID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["role"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["datePledge"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["dateRevoked"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["contact"], "yes")
        self.assertEqual(response.json["ProjectStaff"][0]["inactive"], "no")
        self.assertEqual(response.json["ProjectStaff"][0]["humanSubjectTrainingExp"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["humanSubjectTrainingTypeID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["studyRole"], 1)

    def test_get_staff(self):
        response = self.client.get("/api/projectstaff/1/")
        self.assertEqual(response.json["staffRoleID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["role"], 1)
        self.assertEqual(response.json["datePledge"], "2016-02-02")
        self.assertEqual(response.json["dateRevoked"], "2016-02-02")
        self.assertEqual(response.json["contact"], "yes")
        self.assertEqual(response.json["inactive"], "no")
        self.assertEqual(response.json["humanSubjectTrainingExp"], "2016-02-02")
        self.assertEqual(response.json["humanSubjectTrainingTypeID"], 1)
        self.assertEqual(response.json["studyRole"], 1)
        
    def test_update_staff(self):
        response = self.client.put("/api/projectstaff/1/", data = {
            "staffRoleID" : 2,
            "projectID" : 2,
            "staffID" : 2,
            "role" : 2,
            "datePledge" : "2016-02-03",
            "dateRevoked" : "2016-02-03",
            "contact" : "no",
            "inactive" : "yes",
            "humanSubjectTrainingExp" : "2016-02-03",
            "humanSubjectTrainingTypeID" : 2,
            "studyRole" : 2
        })
        self.assertEqual(response.json["staffRoleID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["role"], 2)
        self.assertEqual(response.json["datePledge"], "2016-02-03")
        self.assertEqual(response.json["dateRevoked"], "2016-02-03")
        self.assertEqual(response.json["contact"], "no")
        self.assertEqual(response.json["inactive"], "yes")
        self.assertEqual(response.json["humanSubjectTrainingExp"], "2016-02-03")
        self.assertEqual(response.json["humanSubjectTrainingTypeID"], 2)
        self.assertEqual(response.json["studyRole"], 2)
        
    def test_delete_staff(self):
        response = self.client.delete("/api/projectstaff/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStaffID 1 deleted")       
              
class TestProjectStatus(PopulatedDB):
    def test_get_project_statuses(self):
        response = self.client.get("/api/projectstatuses/")
        self.assertEqual(response.json["ProjectStatuses"][0]["projectStatusTypeID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["statusDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectStatuses"][0]["statusNotes"], "notes")
        
    def test_get_project_status(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json["projectStatusID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["statusDate"], "2016-02-02")
        self.assertEqual(response.json["statusNotes"], "notes")
        
    def test_update_project_status(self):
        response = self.client.put("/api/projectstatuses/1/", data = {
            "projectStatusTypeID" : 2,
            "projectID": 2,
            "staffID" : 2,
            "statusDate" : "2016-02-03",
            "statusNotes": "notes Updated"
        })
        print(response.json)
        self.assertEqual(response.json["projectStatusTypeID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["statusDate"], "2016-02-03")
        self.assertEqual(response.json["statusNotes"], "notes Updated")
        
    def test_delete_project_status(self):
        response = self.client.delete("/api/projectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusID 1 deleted")       
        
class TestProjectStatusType(PopulatedDB):
    def test_get_project_status_types(self):
        response = self.client.get("/api/projectstatustypes/")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatusTypeID"], 1)
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatus"], "Status 1")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatusDefinition"], "status def")
        
    def test_get_project_status_type(self):
        response = self.client.get("/api/projectstatustypes/1/")
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["projectStatus"], "Status 1")
        self.assertEqual(response.json["projectStatusDefinition"], "status def")
        
    def test_update_project_status_type(self):
        response = self.client.put("/api/projectstatustypes/1/", data = {
            "projectStatus" : "Status 1 Updated",
            "projectStatusDefinition" : "status def Updated"
        })
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["projectStatus"], "Status 1 Updated")
        self.assertEqual(response.json["projectStatusDefinition"], "status def Updated")
        
    def test_delete_project_status_type(self):
        response = self.client.delete("/api/projectstatustypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusTypeID 2 deleted")
 
class TestProjectType(PopulatedDB):
    def test_get_project_types(self):
        response = self.client.get("/api/projecttypes/")
        self.assertEqual(response.json["ProjectTypes"][0]["projectType"], "Type 1")
        self.assertEqual(response.json["ProjectTypes"][0]["projectTypeDefinition"], "Def 1")
        
    def test_get_project_type(self):
        response = self.client.get("/api/projecttypes/1/")
        self.assertEqual(response.json["projectType"], "Type 1")
        self.assertEqual(response.json["projectTypeDefinition"], "Def 1")
        
    def test_update_project_type(self):
        response = self.client.put("/api/projecttypes/1/", data = {
            "projectType" : "2",
            "projectTypeDefinition" : "type def Updated"
        })
        self.assertEqual(response.json["projectType"], "2")
        self.assertEqual(response.json["projectTypeDefinition"], "type def Updated")
        
    def test_delete_project_type(self):
        response = self.client.delete("/api/projecttypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectTypeID 2 deleted")
 
class TestRCStatusList(PopulatedDB):
    def test_get_rcStatusList(self):
        response = self.client.get("/api/rcstatuslist/")
        self.assertEqual(response.json["RCStatusList"][0]["rcStatusID"], 1)
        self.assertEqual(response.json["RCStatusList"][0]["rcStatus"], "Status 1")
        self.assertEqual(response.json["RCStatusList"][0]["rcStatusDefinition"], "rc status def")
        
    def test_get_rcStatus(self):
        response = self.client.get("/api/rcstatuslist/1/")
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rcStatus"], "Status 1")
        self.assertEqual(response.json["rcStatusDefinition"], "rc status def")
        
    def test_update_rcStatus(self):
        response = self.client.put("/api/rcstatuslist/1/", data = {
            "rcStatus" : "Status 1 Updated",
            "rcStatusDefinition" : "rc status def Updated"
        })
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rcStatus"], "Status 1 Updated")
        self.assertEqual(response.json["rcStatusDefinition"], "rc status def Updated")
        
    def test_delete_rcStatusList(self):
        response = self.client.delete("/api/rcstatuslist/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCStatusListID 2 deleted")
                     
class TestReviewCommittee(PopulatedDB):
    def test_get_review_committees(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json['reviewCommittees'][0]["projectID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["rcStatusID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["rcListID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["reviewCommitteeNumber"], "1")
        self.assertEqual(response.json['reviewCommittees'][0]["dateInitialReview"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["dateExpires"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["rcNote"], "rc_note")
        self.assertEqual(response.json['reviewCommittees'][0]["rcProtocol"], "rc_proto")
        self.assertEqual(response.json['reviewCommittees'][0]["rcApproval"], "rc_approval")
        
    def test_get_review_committee(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rcListID"], 1)
        self.assertEqual(response.json["reviewCommitteeNumber"], "1")
        self.assertEqual(response.json["dateInitialReview"], "2016-02-02")
        self.assertEqual(response.json["dateExpires"], "2016-02-02")
        self.assertEqual(response.json["rcNote"], "rc_note")
        self.assertEqual(response.json["rcProtocol"], "rc_proto")
        self.assertEqual(response.json["rcApproval"], "rc_approval")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommittees/1/", data = {
            "projectID" : 2,
            "rcStatusID": 2,
            "rcListID": 2,
            "reviewCommitteeNumber":"2",
            "dateInitialReview":"2016-02-03",
            "dateExpires" : "2016-02-03",
            "rcNote" : "rc_note Updated",
            "rcProtocol" : "rc_proto Updated",
            "rcApproval":"rc_approval Updated"
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["rcStatusID"], 2)
        self.assertEqual(response.json["rcListID"], 2)
        self.assertEqual(response.json["reviewCommitteeNumber"], "2")
        self.assertEqual(response.json["dateInitialReview"], "2016-02-03")
        self.assertEqual(response.json["dateExpires"], "2016-02-03")
        self.assertEqual(response.json["rcNote"], "rc_note Updated")
        self.assertEqual(response.json["rcProtocol"], "rc_proto Updated")
        self.assertEqual(response.json["rcApproval"], "rc_approval Updated")
        
    def test_delete_review_committee(self):
        response = self.client.delete("/api/reviewcommittees/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ReviewCommitteeID 1 deleted")
        
class TestReviewCommitteeList(PopulatedDB):
    def test_get_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json["reviewCommitteeList"][0]["reviewCommittee"], "rc 1")
        self.assertEqual(response.json["reviewCommitteeList"][0]["rcDescription"], "rc desc 1")
        
    def test_get_review_committee_list(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["reviewCommittee"], "rc 1")
        self.assertEqual(response.json["rcDescription"], "rc desc 1")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommitteelist/1/", data = {
            "reviewCommittee" : "rc Updated",
            "rcDescription" : "rc desc Updated"
            })
        self.assertEqual(response.json["reviewCommittee"],"rc Updated")
        self.assertEqual(response.json["rcDescription"],"rc desc Updated")
        
    def test_delete_review_committee_list(self):
        response = self.client.delete("/api/reviewcommitteelist/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCListID 2 deleted")

class TestStaff(PopulatedDB):
    def test_get_staffs(self):
        response = self.client.get("/api/staff/")
        self.assertEqual(response.json["Staff"][0]["staffID"], 1)
        self.assertEqual(response.json["Staff"][0]["firstName"], "fname")
        self.assertEqual(response.json["Staff"][0]["lastName"], "lname")
        self.assertEqual(response.json["Staff"][0]["middleName"], "middle_name")
        self.assertEqual(response.json["Staff"][0]["email"], "email")
        self.assertEqual(response.json["Staff"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["Staff"][0]["phoneComment"], "phoneComment")
        self.assertEqual(response.json["Staff"][0]["institution"], "institution")
        self.assertEqual(response.json["Staff"][0]["department"], "department")
        self.assertEqual(response.json["Staff"][0]["position"], "position")
        self.assertEqual(response.json["Staff"][0]["credentials"], "credentials")
        self.assertEqual(response.json["Staff"][0]["street"], "street")
        self.assertEqual(response.json["Staff"][0]["city"], "city")
        self.assertEqual(response.json["Staff"][0]["humanSubjectTrainingExp"], "2016-02-02")
        self.assertEqual(response.json["Staff"][0]["ucrRole"], 1)

    def test_get_staff(self):
        response = self.client.get("/api/staff/1/")
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["middleName"], "middle_name")
        self.assertEqual(response.json["email"], "email")
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneComment"], "phoneComment")
        self.assertEqual(response.json["institution"], "institution")
        self.assertEqual(response.json["department"], "department")
        self.assertEqual(response.json["position"], "position")
        self.assertEqual(response.json["credentials"], "credentials")
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["humanSubjectTrainingExp"], "2016-02-02")
        self.assertEqual(response.json["ucrRole"], 1)
        
    def test_update_staff(self):
        response = self.client.put("/api/staff/1/", data = {
            "firstName" : "fname2",
            "lastName" : "lname2",
            "middleName" : "middle_name2",
            "email" : "email2",
            "phoneNumber" : "phone2",
            "phoneComment" : "phoneComment2",
            "institution" : "institution2",
            "department" : "department2",
            "position" : "position2",
            "credentials" : "credentials2",
            "street" : "street2",
            "city" : "city2",
            "state" : "state2",
            "humanSubjectTrainingExp" : "2016-02-03",
            "ucrRole" : 2
            })
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["firstName"], "fname2")
        self.assertEqual(response.json["lastName"], "lname2")
        self.assertEqual(response.json["middleName"], "middle_name2")
        self.assertEqual(response.json["email"], "email2")
        self.assertEqual(response.json["phoneNumber"], "phone2")
        self.assertEqual(response.json["phoneComment"], "phoneComment2")
        self.assertEqual(response.json["institution"], "institution2")
        self.assertEqual(response.json["department"], "department2")
        self.assertEqual(response.json["position"], "position2")
        self.assertEqual(response.json["credentials"], "credentials2")
        self.assertEqual(response.json["street"], "street2")
        self.assertEqual(response.json["city"], "city2")
        self.assertEqual(response.json["humanSubjectTrainingExp"], "2016-02-03")
        self.assertEqual(response.json["ucrRole"], 2)
        
    def test_delete_staff(self):
        response = self.client.delete("/api/staff/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffID 2 deleted")

class TestStaffRole(PopulatedDB):
    def test_get_staff_roles(self):
        response = self.client.get("/api/staffroles/")
        self.assertEqual(response.json["StaffRoles"][0]["staffRoleID"], 1)
        self.assertEqual(response.json["StaffRoles"][0]["staffRole"], "role")
        self.assertEqual(response.json["StaffRoles"][0]["staffRoleDescription"], "desc")

    def test_get_staff_role(self):
        response = self.client.get("/api/staffroles/1/")
        self.assertEqual(response.json["staffRoleID"], 1)
        self.assertEqual(response.json["staffRole"], "role")
        self.assertEqual(response.json["staffRoleDescription"], "desc")
        
    def test_update_staff_role(self):
        response = self.client.put("/api/staffroles/1/", data = {
            "staffRole" : "role Updated",
            "staffRoleDescription" : "desc Updated",
            })
        self.assertEqual(response.json["staffRoleID"], 1)
        self.assertEqual(response.json["staffRole"], "role Updated")
        self.assertEqual(response.json["staffRoleDescription"], "desc Updated")
        
    def test_delete_staff_role(self):
        response = self.client.delete("/api/staffroles/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffRoleID 2 deleted")
           
class TestStaffTraining(PopulatedDB):
    def test_get_staff_trainings(self):
        response = self.client.get("/api/stafftrainings/")
        self.assertEqual(response.json["StaffTrainings"][0]["staffTrainingID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["staffID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["dateTaken"], "2016-02-02")
        self.assertEqual(response.json["StaffTrainings"][0]["dateExpires"], "2016-02-02")

    def test_get_staff_training(self):
        response = self.client.get("/api/stafftrainings/1/")
        self.assertEqual(response.json["staffTrainingID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["dateTaken"], "2016-02-02")
        self.assertEqual(response.json["dateExpires"], "2016-02-02")
        
    def test_update_staff_training(self):
        response = self.client.put("/api/stafftrainings/1/", data = {
            "staffID" : 2,
            "humanSubjectTrainingID" : 2,
            "dateTaken" : "2016-02-03",
            "dateExpires" : "2016-02-03"
            })
        self.assertEqual(response.json["staffTrainingID"], 1)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["humanSubjectTrainingID"], 2)
        self.assertEqual(response.json["dateTaken"], "2016-02-03")
        self.assertEqual(response.json["dateExpires"], "2016-02-03")
        
    def test_delete_staff_training(self):
        response = self.client.delete("/api/stafftrainings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffTrainingID 1 deleted")
           
class TestTracing(PopulatedDB):
    def test_get_tracings(self):
        response = self.client.get("/api/tracings/")
        self.assertEqual(response.json["Tracings"][0]["tracingID"], 1)
        self.assertEqual(response.json["Tracings"][0]["tracingSourceID"], 1)
        self.assertEqual(response.json["Tracings"][0]["projectPatientID"], 1)
        self.assertEqual(response.json["Tracings"][0]["date"], "2016-02-02")
        self.assertEqual(response.json["Tracings"][0]["staff"], 1)
        self.assertEqual(response.json["Tracings"][0]["notes"], "notes")
        
    def test_get_tracing(self):
        response = self.client.get("/api/tracings/1/")
        self.assertEqual(response.json["tracingID"], 1)
        self.assertEqual(response.json["tracingSourceID"], 1)
        self.assertEqual(response.json["projectPatientID"], 1)
        self.assertEqual(response.json["date"], "2016-02-02")
        self.assertEqual(response.json["staff"], 1)
        self.assertEqual(response.json["notes"], "notes")
        
    def test_update_tracing(self):
        response = self.client.put("/api/tracings/1/", data = {
            "tracingSourceID" : 2,
            "projectPatientID" : 2,
            "date" : "2016-02-03",
            "staff" : 2,
            "notes" : "notes Updated"
            })
        self.assertEqual(response.json["tracingID"], 1)
        self.assertEqual(response.json["tracingSourceID"], 2)
        self.assertEqual(response.json["projectPatientID"], 2)
        self.assertEqual(response.json["date"], "2016-02-03")
        self.assertEqual(response.json["staff"], 2)
        self.assertEqual(response.json["notes"], "notes Updated")
        
    def test_delete_tracing(self):
        response = self.client.delete("/api/tracings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "TracingID 1 deleted")
                     
class TestTracingSource(PopulatedDB):
    def test_get_tracing_sources(self):
        response = self.client.get("/api/tracingsources/")
        self.assertEqual(response.json["TracingSources"][0]["tracingSourceID"], 1)
        self.assertEqual(response.json["TracingSources"][0]["description"], "desc")
        
    def test_get_tracing_source(self):
        response = self.client.get("/api/tracingsources/1/")
        self.assertEqual(response.json["tracingSourceID"], 1)
        self.assertEqual(response.json["description"], "desc")
        
    def test_update_tracing_source(self):
        response = self.client.put("/api/tracingsources/1/", data = {
            "description" : "desc Updated"
            })
        self.assertEqual(response.json["tracingSourceID"], 1)
        self.assertEqual(response.json["description"], "desc Updated")
        
    def test_delete_tracing_source(self):
        response = self.client.delete("/api/tracingsources/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "TracingSourceID 2 deleted")
        
class TestUCRReport(PopulatedDB):
    def test_get_ucr_reports(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json["ucrReports"][0]["projectID"],1)
        self.assertEqual(response.json["ucrReports"][0]["reportType"],1)
        self.assertEqual(response.json["ucrReports"][0]["reportSubmitted"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["reportDue"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["reportDoc"],"doc")
        
    def test_get_ucr_report(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["reportType"],1)
        self.assertEqual(response.json["reportSubmitted"],"2016-02-02")
        self.assertEqual(response.json["reportDue"],"2016-02-02")
        self.assertEqual(response.json["reportDoc"],"doc")
        
    def test_update_ucr_report(self):
        response = self.client.put("/api/ucrreports/1/", data = {
            "projectID" : 2,
            "reportType": 2,
            "reportSubmitted": "2016-02-03",
            "reportDue": "2016-02-03",
            "reportDoc": "doc Updated"
        })
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["reportType"],2)
        self.assertEqual(response.json["reportSubmitted"],"2016-02-03")
        self.assertEqual(response.json["reportDue"],"2016-02-03")
        self.assertEqual(response.json["reportDoc"],"doc Updated")
        
    def test_delete_ucr_report(self):
        response = self.client.delete("/api/ucrreports/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "UcrReportID 1 deleted")
        
        
        
if __name__ == '__main__':
    unittest.main()