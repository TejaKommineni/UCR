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
        return app.create_app('../tests/test_config.py')

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db2()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_informant_relationships(self):
        relationships = []
        relationships.append(models.InformantRelationship(
            informantRelationship="Mother"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Father"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Son"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Daughter"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Grandson"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Granddaughter"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Uncle"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Aunt"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Cousin"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Wife"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Husband"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Friend"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Other Family Member"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Other"
        ))
        return relationships

    def create_final_codes(self):
        finalCodes = []
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Pending",
            finalCode=0
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Consent- Survey complete w/Med. Rcd. release",
            finalCode=100
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Consent- Survey complete NO Med.Rcd. release",
            finalCode=101
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Consent- Incomplete survey. Cannot complete (see notes for reason)",
            finalCode=111
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Survey complete- no consent form with or without medical release",
            finalCode=112
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- by mail",
            finalCode=200
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no reason",
            finalCode=201

        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- too ill",
            finalCode=202
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no interest",
            finalCode=203
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- too old",
            finalCode=204
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no cancer",
            finalCode=205
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No-upset",
            finalCode=207
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- DO NOT CONTACT-per contact with patient on study",
            finalCode=208
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no signed consent form",
            finalCode=209
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No response after max effort",
            finalCode=300
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Lost to follow-up (bad/no address or phone)-may have contacted once or initial letter not returned, but can no longer contact",
            finalCode=301
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Language Barrier",
            finalCode=302
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No response after 2+ letters (no/bad phone)",
            finalCode=303
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Deceased AFTER selection",
            finalCode=309
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible - Current Age",
            finalCode=400
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-other",
            finalCode=401
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- DX date",
            finalCode=402
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- Patient Deceased",
            finalCode=403
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- mental capacity",
            finalCode=404
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- histology or behavior",
            finalCode=406
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- out of state resident at DX",
            finalCode=407
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-Recently contacted for another UCR study or lost to follow-up in another UCR study within past year",
            finalCode=408
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-out of country",
            finalCode=409
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-Do not contact per DMS",
            finalCode=410
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-Not able to send letter OR letter returned and no other contact possible (for NOK or Patient)",
            finalCode=411
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible - Contacted for other study within 1 year",
            finalCode=412
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Holding",
            finalCode=999
        ))
        return finalCodes

    def create_states(self):
        states = []
        states.append(models.State(
            state="Alabama"
        ))
        states.append(models.State(
            state="Alaska"
        ))
        states.append(models.State(
            state="Arizona"
        ))
        states.append(models.State(
            state="Arkansas"
        ))
        states.append(models.State(
            state="California"
        ))
        states.append(models.State(
            state="Colorado"
        ))
        states.append(models.State(
            state="Connecticut"
        ))
        states.append(models.State(
            state="Delaware"
        ))
        states.append(models.State(
            state="Florida"
        ))
        states.append(models.State(
            state="Georgia"
        ))
        states.append(models.State(
            state="Hawaii"
        ))
        states.append(models.State(
            state="Idaho"
        ))
        states.append(models.State(
            state="Illinois"
        ))
        states.append(models.State(
            state="Indiana"
        ))
        states.append(models.State(
            state="Iowa"
        ))
        states.append(models.State(
            state="Kansas"
        ))
        states.append(models.State(
            state="Kentucky"
        ))
        states.append(models.State(
            state="Louisiana"
        ))
        states.append(models.State(
            state="Maine"
        ))
        states.append(models.State(
            state="Maryland"
        ))
        states.append(models.State(
            state="Massachusetts"
        ))
        states.append(models.State(
            state="Michigan"
        ))
        states.append(models.State(
            state="Minnesota"
        ))
        states.append(models.State(
            state="Mississippi"
        ))
        states.append(models.State(
            state="Missouri"
        ))
        states.append(models.State(
            state="Montana"
        ))
        states.append(models.State(
            state="Nebraska"
        ))
        states.append(models.State(
            state="Nevada"
        ))
        states.append(models.State(
            state="New Hampshire"
        ))
        states.append(models.State(
            state="New Jersey"
        ))
        states.append(models.State(
            state="New Mexico"
        ))
        states.append(models.State(
            state="New York"
        ))
        states.append(models.State(
            state="North Carolina"
        ))
        states.append(models.State(
            state="North Dakota"
        ))
        states.append(models.State(
            state="Ohio"
        ))
        states.append(models.State(
            state="Oklahoma"
        ))
        states.append(models.State(
            state="Oregon"
        ))
        states.append(models.State(
            state="Pennsylvania"
        ))
        states.append(models.State(
            state="Rhhode Island"
        ))
        states.append(models.State(
            state="South Carolina"
        ))
        states.append(models.State(
            state="South Dakota"
        ))
        states.append(models.State(
            state="Tennessee"
        ))
        states.append(models.State(
            state="Texas"
        ))
        states.append(models.State(
            state="Utah"
        ))
        states.append(models.State(
            state="Vermont"
        ))
        states.append(models.State(
            state="Virginia"
        ))
        states.append(models.State(
            state="Washington"
        ))
        states.append(models.State(
            state="West Virginia"
        ))
        states.append(models.State(
            state="Wisonsin"
        ))
        states.append(models.State(
            state="Wyoming"
        ))
        states.append(models.State(
            state="District of Columbia"
        ))
        return states

    def create_abstract_statuses(self):
        statuses = []
        statuses.append(models.AbstractStatus(
            abstractStatus="Pending"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Eligible, Assigned to Abstractor"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Eligible, Received"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Complete"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Refused (no medical release)"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Not Included In Abstraction"
        ))
        return statuses

    def create_sexes(self):
        sexes = []
        sexes.append(models.Sex(
            sex="Female"
        ))
        sexes.append(models.Sex(
            sex="Male"
        ))
        sexes.append(models.Sex(
            sex="Transsexual"
        ))
        sexes.append(models.Sex(
            sex="Unknown"
        ))
        return sexes

    def create_races(self):
        races = []
        races.append(models.Race(
            race="American Indian or Alaska Native"
        ))
        races.append(models.Race(
            race="Asian"
        ))
        races.append(models.Race(
            race="Black"
        ))
        races.append(models.Race(
            race="Native Hawaiian or Other Pacific Islander"
        ))
        races.append(models.Race(
            race="White"
        ))
        races.append(models.Race(
            race="Unknown"
        ))
        return races

    def create_ethnicities(self):
        ethnicities = []
        ethnicities.append(models.Ethnicity(
            ethnicity="Hispanic or Latino"
        ))
        ethnicities.append(models.Ethnicity(
            ethnicity="Not Hispanic or Latino"
        ))
        ethnicities.append(models.Ethnicity(
            ethnicity="Unknown"
        ))
        return ethnicities

    def create_vital_statuses(self):
        vitals = []
        vitals.append(models.VitalStatus(
            vitalStatus="Alive"
        ))
        vitals.append(models.VitalStatus(
            vitalStatus="Dead"
        ))
        return vitals

    def create_contacts(self):
        contacts = []
        contacts.append(models.Contacts(
            contact="yes"
        ))
        contacts.append(models.Contacts(
            contact="no"
        ))
        return contacts

    def create_inactives(self):
        inactives = []
        inactives.append(models.Inactive(
            inactive="Yes"
        ))
        inactives.append(models.Inactive(
            inactive="No"
        ))
        return inactives

    def create_ucr_report_types(self):
        reports = []
        reports.append(models.UCRReportType(
            ucrReportType="Report 1"
        ))
        reports.append(models.UCRReportType(
            ucrReportType="Report 2"
        ))
        return reports

    def create_physician_statuses(self):
        statuses = []
        statuses.append(models.PhysicianStatus(
            physicianStatus="active"
        ))
        statuses.append(models.PhysicianStatus(
            physicianStatus="inactive"
        ))
        return statuses

    def create_physician_facility_statuses(self):
        statuses = []
        statuses.append(models.PhysicianFacilityStatus(
            physicianFacilityStatus="open"
        ))
        statuses.append(models.PhysicianFacilityStatus(
            physicianFacilityStatus="closed"
        ))
        return statuses

    def create_phone_types(self):
        phoneTypes = []
        phoneTypes.append(models.PhoneTypeLUT(
            phoneType="cell"
        ))
        phoneTypes.append(models.PhoneTypeLUT(
            phoneType="home"
        ))
        phoneTypes.append(models.PhoneTypeLUT(
            phoneType="work"
        ))
        return phoneTypes

    def create_irb_holders(self):
        holders = []
        holders.append(models.IRBHolderLUT(
            holder="U of U",
            holderDefinition="U of U researcher is responsible for IRB"
        ))
        holders.append(models.IRBHolderLUT(
            holder="External",
            holderDefinition="External researcher is responsible for IRB"
        ))
        holders.append(models.IRBHolderLUT(
            holder="UCR",
            holderDefinition="UCR is responsible for IRB. IRB is in UCR researcher's name"
        ))
        holders.append(models.IRBHolderLUT(
            holder="N/A",
            holderDefinition="Not Applicable"
        ))
        holders.append(models.IRBHolderLUT(
            holder="Unknown",
            holderDefinition="Unknown"
        ))
        holders.append(models.IRBHolderLUT(
            holder="Other",
            holderDefinition="Other"
        ))
        return holders

    def create_project_types(self):
        types = []
        types.append(models.ProjectType(
            projectType="Consent",
            projectTypeDefinition="UCR obtains patient consent for project"
        ))
        types.append(models.ProjectType(
            projectType="Permission",
            projectTypeDefinition="UCR obtains patient permission for project"
        ))
        types.append(models.ProjectType(
            projectType="Linkage",
            projectTypeDefinition="UCR conducts data linkage. No patient contact"
        ))
        types.append(models.ProjectType(
            projectType="Physician",
            projectTypeDefinition="UCR contacts physicians only. No patient contact."
        ))
        types.append(models.ProjectType(
            projectType="Other",
            projectTypeDefinition="Need to clean up"
        ))
        types.append(models.ProjectType(
            projectType="Unknown",
            projectTypeDefinition="When still in application phase"
        ))
        types.append(models.ProjectType(
            projectType="Tumor",
            projectTypeDefinition="UCR creates a tumor level data file.  No patient contact. No linkage conducted"
        ))
        return types

    def create_contact_statuses(self):
        contactInfoStatuses = []
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Current"
        ))
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Unknown"
        ))
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Bad"
        ))
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Duplicate"
        ))
        return contactInfoStatuses

    def create_contact_sources(self):
        contactSources = []
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="UCR"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="UPDB"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Patient or NOK"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Research"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="USPS"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Bad"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Accurint"
        ))
        return contactSources

    def create_grant_statuses(self):
        statuses = []
        statuses.append(models.GrantStatusLUT(
            grantStatus="Submitted"
        ))
        statuses.append(models.GrantStatusLUT(
            grantStatus="Awarded"
        ))
        statuses.append(models.GrantStatusLUT(
            grantStatus="Rejected"
        ))
        return statuses

    def create_funding_sources(self):
        sources = []
        sources.append(models.FundingSourceLUT(
            fundingSource="NCI"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="NCI-Pilot"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="U of U Department"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="SEER"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="UDOH"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="AHRQ"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="PCORI"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="CHOICE"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="Private Industry"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="NIH"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="Primary Children's Hospital Foundation"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="United BioSource Corporation"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="Novo Nordisk"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="RTI"
        ))
        return sources

    def create_review_committee_statuses(self):
        statuses = []
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Pending",
            reviewCommitteeStatusDefinition="Pending"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Approved",
            reviewCommitteeStatusDefinition="Approved"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Closed",
            reviewCommitteeStatusDefinition="Closed"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Non Human Subject",
            reviewCommitteeStatusDefinition="Non Human Subject"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Exempt",
            reviewCommitteeStatusDefinition="Exempt"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Signed",
            reviewCommitteeStatusDefinition="Signed"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Sent - Carol",
            reviewCommitteeStatusDefinition="Sent - Carol"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Not Needed",
            reviewCommitteeStatusDefinition="Not Needed"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Sent - Full ARC Review",
            reviewCommitteeStatusDefinition="Sent - Full ARC Review"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Unknown",
            reviewCommitteeStatusDefinition="Unknown"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Expired",
            reviewCommitteeStatusDefinition="Expired"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Submitted",
            reviewCommitteeStatusDefinition="Submitted"
        ))
        return statuses

    def create_project_statuses(self):
        statuses = []
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Pending",
            projectStatusDefinition="Project has not started"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Active",
            projectStatusDefinition="Project is underway"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Hibernate",
            projectStatusDefinition="Project has open IRB, but no current UCR activity"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="IRB Closed",
            projectStatusDefinition="IRB is closed. Project is closed."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Archived",
            projectStatusDefinition="Project is old and inactive for years. IRB is closed."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Canceled",
            projectStatusDefinition="Project never materialized."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Pre-Application",
            projectStatusDefinition="Received pre-application"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Application",
            projectStatusDefinition="Application under review"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Post-Contact",
            projectStatusDefinition="Only for contact studies: Contact complete but we are still reviewing pubs and/or linking data."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Linkage",
            projectStatusDefinition="Regularly Scheduled Linkages"
        ))
        return statuses

    def create_log_subjects(self):
        subjects = []
        subjects.append(models.LogSubjectLUT(
            logSubject="Review Committee"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Budget"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Misc."
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Data"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Pre-Application"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Application"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Recruitment"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Audit"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Start-up"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Publication"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Close-out"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Agreements"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Reports"
        ))
        return subjects

    def create_review_committees(self):
        rcs = []
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="U of U IRB",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="ARC",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="IHC",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="St Marks",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Odgen",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="IASIS",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Vanderbuilt",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Emory",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Admin",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="RTI",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Loma Linda University",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="NCI-CDA",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Sterling",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Research Agreement",
            reviewCommitteeDescription="Expires after 5 years"
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Research Application",
            reviewCommitteeDescription="Renewed annually"
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Annual Report",
            reviewCommitteeDescription="Annually"
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Research Proposal",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="RGE",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Westat",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UDOH Data Use Committees",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="OHSRP - NIH Office of Human Subjects Research",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UDOH IRB",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UDOH Health Data Committee",
            reviewCommitteeDescription=None
        ))
        return rcs

    def create_staff_roles(self):
        roles = []
        roles.append(models.StaffRoleLUT(
            staffRole="PI-External",
            staffRoleDescription="Principle Investigator- external, no U of U affiliation"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Co-PI",
            staffRoleDescription="Co-PI"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Coordinator",
            staffRoleDescription="Runs study for investigator"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Research Assistant",
            staffRoleDescription="Assists on study"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Research Associate",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="UCR Staff",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Data Analyst",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="PI-U of U",
            staffRoleDescription="Principle Investigator- U of U affiliation"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="PI-UCR",
            staffRoleDescription="Principle Investigator- UCR Researcher"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="PPR Staff",
            staffRoleDescription="UPDB Staff"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Programmer",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Adminstrative Staff",
            staffRoleDescription="No access to confidential data manages budget etc."
        ))
        return roles

    def create_project_phases(self):
        phases = []
        phases.append(models.PhaseStatus(
            phaseStatus="Received",
            phaseDescription="Items received from investigator"
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Meeting Scheduled",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="In Review",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="ARC Approved",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Sent to ARC",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Sent to Carol",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Sent to Investigator",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Contract Signed",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="SOP Complete",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Approval",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="RGE Approval",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Annual Review Received",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Notified Carrie Database Needed",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Project Lead Assigned",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Project Lead Assigned",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Study Complete",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Meeting",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Invoice Sent",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Data Transfer",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Report to Researcher",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Approved/Agreed",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Email/Phone from CRO",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Continuing Review",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="OSP",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Study Activities",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Accounting",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Amendment",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Email",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Report In Progress",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Report Sent",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Submitted",
            phaseDescription=None
        ))
        return phases

    def create_human_subject_trainings(self):
        hsts = []
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="CITI"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="NIH"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="VA"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="Unknown"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="N/A"
        ))
        return hsts

    def create_tracing_sources(self):
        sources = []
        sources.append(models.TracingSourceLUT(
            description="DMS"
        ))
        sources.append(models.TracingSourceLUT(
            description="Filer4"
        ))
        sources.append(models.TracingSourceLUT(
            description="DEX/White pages"
        ))
        sources.append(models.TracingSourceLUT(
            description="Intellus"
        ))
        sources.append(models.TracingSourceLUT(
            description="Dr Office"
        ))
        sources.append(models.TracingSourceLUT(
            description="Voter DB"
        ))
        sources.append(models.TracingSourceLUT(
            description="Zaba"
        ))
        sources.append(models.TracingSourceLUT(
            description="Other (Enter in Notes)"
        ))
        sources.append(models.TracingSourceLUT(
            description="Obit"
        ))
        sources.append(models.TracingSourceLUT(
            description="Advance Bkground Check"
        ))
        return sources

    def create_contact_types(self):
        contact_types = []
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed 1st packet to patient (intro letter, survey, consent, med rcd. release)",
            contactCode=100
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed Reminder letter",
            contactCode=101
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed 2nd packet (FU letter, survey, consent, med rcd release)",
            contactCode=102
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed Thank you letter and copy of consent form",
            contactCode=103
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed Packet (after phone contact)",
            contactCode=109
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed additional items- (survey, consent form, envelope, etc)",
            contactCode=110
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Undeliverable, mail returned w/forwarding addresses, mailed to new address",
            contactCode=150
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Undeliverable, Mail returned, NO forwarding address",
            contactCode=151
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Packet Returned - Temporarily Away",
            contactCode=152
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Left voicemail",
            contactCode=200
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Left message with person",
            contactCode=201
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="No answer",
            contactCode=202
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Busy",
            contactCode=203
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Bad Phone number",
            contactCode=204
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Received, thinking about it",
            contactCode=205
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Received, willing",
            contactCode=206
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Received, already sent to us",
            contactCode=207
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- too sick",
            contactCode=208
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- no cancer",
            contactCode=209
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Language Barrier",
            contactCode=210
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Deceased",
            contactCode=211
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Pt unable to come to phone, could not leave message",
            contactCode=212
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Incompetent",
            contactCode=213
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Patient left message for Coordinator",
            contactCode=214
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Refused (no reason given)",
            contactCode=215
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Ineligible",
            contactCode=216
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- did not receive, mailed another letter",
            contactCode=217
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Other",
            contactCode=218
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Survey returned without consent form",
            contactCode=300
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Survey returned incomplete",
            contactCode=301
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Consent returned without survey",
            contactCode=302
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Received consent, survey received previously",
            contactCode=304
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Enter in error",
            contactCode=999
        ))
        return contact_types

    def create_ucr_roles(self):
        roles = []
        roles.append(models.UCRRole(
            ucrRole="role 1"
        ))
        roles.append(models.UCRRole(
            ucrRole="role 2"
        ))
        return roles

    def create_gift_cards(self):
        gcs = []
        gcs.append(models.GiftCard(
            description="Smiths Gift Card",
            barcode="123456789",
            amount=25
        ))
        gcs.append(models.GiftCard(
            description="Smiths Gift Card",
            barcode="123456788",
            amount=25
        ))
        gcs.append(models.GiftCard(
            description="Smiths Gift Card",
            barcode="123456787",
            amount=25
        ))
        return gcs

    def create_users(self):
        users = []
        users.append(models.User(
            uID="u0973461",
            roleID=2  # developer
        ))
        users.append(models.User(
            uID="u0050151",
            roleID=1  # Contact Staff
        ))
        return users

    def populate_db2(self):
        """
        This creates the database/tables and populates it with junk data for testing
        :return:
        """
        db.create_all()

        informantRelationships = self.create_informant_relationships()
        users = self.create_users()
        finalCodes = self.create_final_codes()
        states = self.create_states()
        abstractStatuses = self.create_abstract_statuses()
        sexes = self.create_sexes()
        races = self.create_races()
        ethnicities = self.create_ethnicities()
        vitals = self.create_vital_statuses()
        contacts = self.create_contacts()
        inactives = self.create_inactives()
        ucrReportTypes = self.create_ucr_report_types()
        physicianStatuses = self.create_physician_statuses()
        physFacilityStatuses = self.create_physician_facility_statuses()
        phoneTypes = self.create_phone_types()
        irbHolders = self.create_irb_holders()
        projectTypes = self.create_project_types()
        contactStatuses = self.create_contact_statuses()
        contactSources = self.create_contact_sources()
        grantStatuses = self.create_grant_statuses()
        fundingSources = self.create_funding_sources()
        reviewCommitteeStatuses = self.create_review_committee_statuses()
        projectStatuses = self.create_project_statuses()
        logTypes = self.create_log_subjects()
        reviewCommittees = self.create_review_committees()
        staffRoles = self.create_staff_roles()
        projectPhases = self.create_project_phases()
        hsts = self.create_human_subject_trainings()
        tracingSources = self.create_tracing_sources()
        contactTypes = self.create_contact_types()
        ucrRoles = self.create_ucr_roles()
        giftCards = self.create_gift_cards()

        project1 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        project2 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        budget1 = models.Budget(
            projectID=1,
            numPeriods=1,
            periodStart=datetime(2016, 2, 2),
            periodEnd=datetime(2016, 2, 2),
            periodTotal=1.23,
            periodComment="comment")

        rc = models.ReviewCommittee(
            projectID=1,
            reviewCommitteeStatusID=1,
            reviewCommitteeLUTID=1,
            reviewCommitteeNumber="1",
            dateInitialReview=datetime(2016, 2, 2),
            dateExpires=datetime(2016, 2, 2),
            rcNote="rc_note",
            rcProtocol="rc_proto",
            rcApproval="rc_approval")

        ucr = models.UCRReport(
            projectID=1,
            reportTypeID=1,
            reportSubmitted=datetime(2016, 2, 2),
            reportDue=datetime(2016, 2, 2),
            reportDoc="doc"
        )
        arcReview = models.ArcReview(
            projectID=1,
            reviewType=1,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)

        funding = models.Funding(
            grantStatusID=1,
            projectID=1,
            fundingSourceID=1,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )
        staff2 = models.Staff(
            userID=2,
            firstName="Phoebe",
            lastName="",
            middleName="McNeally",
            email="email",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=2,
            ucrRoleID=1
        )

        projStatus = models.ProjectStatus(
            projectStatusTypeID=1,
            projectID=1,
            staffID=1,
            statusDate=datetime(2016, 2, 2),
            statusNotes="notes"
        )

        preApp = models.PreApplication(
            projectID=1,
            piFirstName="pi_fname",
            piLastName="pi_lname",
            piEmail="pi_email",
            piPhone="pi_phone",
            contactFirstName="contact_fname",
            contactLastName="contact_lname",
            contactPhone="contact_phone",
            contactEmail="contact_email",
            institution="institution",
            institution2="institution2",
            uid="uid",
            udoh=1,
            projectTitle="project_title",
            purpose="purpose",
            irb0=True,
            irb1=True,
            irb2=True,
            irb3=True,
            irb4=True,
            otherIrb="other_irb",
            updb=True,
            ptContact=True,
            startDate=datetime(2016, 2, 2),
            link=True,
            deliveryDate=datetime(2016, 2, 2),
            description="description"
        )
        log = models.Log(
            logSubjectID=1,
            projectID=1,
            staffID=1,
            phaseStatusID=1,
            note="note",
            date=datetime(2016, 2, 2)
        )
        projectStaff = models.ProjectStaff(
            staffRoleID=1,
            projectID=1,
            staffID=1,
            datePledge=datetime(2016, 2, 2),
            dateRevoked=datetime(2016, 2, 2),
            contactID=1,
            inactiveID=1
        )
        staffTraining = models.StaffTraining(
            staffID=1,
            humanSubjectTrainingID=1,
            dateTaken=datetime(2016, 2, 2),
            dateExpires=datetime(2016, 2, 2)
        )
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname",
            lastName="lname",
            middleName="mname",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=15,
            dobMonth=2,
            dobYear=1990,
            SSN="999999999",
            sexID=2,
            raceID=1,
            ethnicityID=1,
            vitalStatusID=1
        )
        patient2 = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )

        patientAddress = models.PatientAddress(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            street="street",
            street2="street2",
            city="city",
            stateID=1,
            zip="12345",
            addressStatusDate=datetime(2016, 2, 2),
        )

        patientEmail = models.PatientEmail(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            email="email",
            emailStatusDate=datetime(2016, 2, 2)
        )
        patientPhone = models.PatientPhone(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
        patientPhone2 = models.PatientPhone(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
        informant1 = models.Informant(
            participantID=1,
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            informantPrimary=True,
            informantRelationshipID=1,
            notes="notes"
        )
        informant2 = models.Informant(
            participantID=1,
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            informantPrimary=True,
            informantRelationshipID=1,
            notes="notes"
        )
        informantAddress = models.InformantAddress(
            contactInfoSourceID=1,
            informantID=1,
            contactInfoStatusID=1,
            street="street",
            street2="street2",
            city="city",
            stateID=2,
            zip="12345",
            addressStatusDate=datetime(2016, 2, 2),
        )
        informantPhone = models.InformantPhone(
            contactInfoSourceID=1,
            informantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
        informantPhone2 = models.InformantPhone(
            contactInfoSourceID=1,
            informantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip=99999,
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )
        ctc2 = models.CTC(
            participantID=1,
            dxDateDay=3,
            dxDateMonth=10,
            dxDateYear=1958,
            site="Site 1",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=2,
            dxZip=99999,
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc123"
        )
        projectPatient = models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrp=1,
            finalCodeID=1,
            finalCodeDate=datetime(2016, 2, 2),
            enrollmentDate=datetime(2016, 2, 2),
            dateCoordSigned=datetime(2016, 2, 2),
            importDate=datetime(2016, 2, 2),
            finalCodeStaffID=1,
            enrollmentStaffID=1,
            dateCoordSignedStaffID=1,
            abstractStatusID=1,
            abstractStatusDate=datetime(2016, 2, 2),
            abstractStatusStaffID=1,
            sentToAbstractorDate=datetime(2016, 2, 2),
            sentToAbstractorStaffID=1,
            abstractedDate=datetime(2016, 2, 2),
            abstractorStaffID=1,
            researcherDate=datetime(2016, 2, 2),
            researcherStaffID=1,
            consentLink="link",
            medRecordReleaseSigned=True,
            medRecordReleaseLink="link",
            medRecordReleaseStaffID=1,
            medRecordReleaseDate=datetime(2016, 2, 2),
            surveyToResearcher=datetime(2016, 2, 2),
            surveyToResearcherStaffID=1,
            qualityControl=True,
        )

        projectPatient2 = models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrp=1,
            finalCodeID=1,
            finalCodeDate=datetime(2016, 2, 2),
            enrollmentDate=datetime(2016, 2, 2),
            dateCoordSigned=datetime(2016, 2, 2),
            importDate=datetime(2016, 2, 2),
            finalCodeStaffID=1,
            enrollmentStaffID=1,
            dateCoordSignedStaffID=1,
            abstractStatusID=1,
            abstractStatusDate=datetime(2016, 2, 2),
            abstractStatusStaffID=1,
            sentToAbstractorDate=datetime(2016, 2, 2),
            sentToAbstractorStaffID=1,
            abstractedDate=datetime(2016, 2, 2),
            abstractorStaffID=1,
            researcherDate=datetime(2016, 2, 2),
            researcherStaffID=1,
            consentLink="link",
            medRecordReleaseSigned=True,
            medRecordReleaseLink="link",
            medRecordReleaseStaffID=1,
            medRecordReleaseDate=datetime(2016, 2, 2),
            surveyToResearcher=datetime(2016, 2, 2),
            surveyToResearcherStaffID=1,
            qualityControl=False
        )

        tracing = models.Tracing(
            tracingSourceID=1,
            participantID=1,
            date=datetime(2016, 2, 2),
            staffID=1,
            notes="notes"
        )
        physician = models.Physician(
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            credentials="credentials",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
        )

        physician2 = models.Physician(
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            credentials="credentials",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
        )
        physicianAddress = models.PhysicianAddress(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            street="street",
            street2="street2",
            city="city",
            stateID=1,
            zip="12345",
            addressStatusDate=datetime(2016, 2, 2),
        )

        physicianEmail = models.PhysicianEmail(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            email="email",
            emailStatusDate=datetime(2016, 2, 2)
        )

        physicianPhone = models.PhysicianPhone(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            phoneNumber="phone",
            phoneTypeID=1,
            phoneStatusDate=datetime(2016, 2, 2)
        )
        physicianPhone2 = models.PhysicianPhone(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            phoneNumber="phone",
            phoneTypeID=1,
            phoneStatusDate=datetime(2016, 2, 2)
        )
        physicianToCTC = models.PhysicianToCTC(
            physicianID=1,
            ctcID=1
        )
        facility1 = models.Facility(
            facilityName="name",
            contactFirstName="fname",
            contactLastName="lname",
            facilityStatus=1,
            facilityStatusDate=datetime(2016, 2, 2),
            contact2FirstName="fname",
            contact2LastName="lname"
        )
        facility2 = models.Facility(
            facilityName="name",
            contactFirstName="fname",
            contactLastName="lname",
            facilityStatus=1,
            facilityStatusDate=datetime(2016, 2, 2),
            contact2FirstName="fname",
            contact2LastName="lname"
        )
        facilityAddress = models.FacilityAddress(
            contactInfoSourceID=1,
            facilityID=1,
            contactInfoStatusID=1,
            street="street",
            street2="street2",
            city="city",
            stateID=1,
            zip="12345",
            addressStatusDate=datetime(2016, 2, 2),
        )

        facilityPhone = models.FacilityPhone(
            contactInfoSourceID=1,
            facilityID=1,
            contactInfoStatusID=1,
            clinicName="clinic",
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
        facilityPhone2 = models.FacilityPhone(
            contactInfoSourceID=1,
            facilityID=1,
            contactInfoStatusID=1,
            clinicName="clinic",
            phoneTypeID=1,
            phoneNumber="phone2",
            phoneStatusDate=datetime(2016, 2, 2)
        )
        patientProjectStatusType1 = models.PatientProjectStatusLUT(
            statusDescription="desc"
        )
        patientProjectStatusType2 = models.PatientProjectStatusLUT(
            statusDescription="desc"
        )
        patientProjectStatus = models.PatientProjectStatus(
            patientProjectStatusTypeID=1,
            participantID=1,
            statusDate=datetime(2016,2,2)
        )
        physicianFacility = models.PhysicianFacility(
            facilityID=1,
            physicianID=1,
            physFacilityStatusID=1,
            physFacilityStatusDate=datetime(2016, 2, 2)
        )
        contact = models.Contact(
            contactTypeLUTID=1,
            participantID=1,
            staffID=1,
            informantID=1,
            informantPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        )
        contact2 = models.Contact(
            contactTypeLUTID=1,
            participantID=1,
            staffID=1,
            facilityID=1,
            facilityPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        )
        contact3 = models.Contact(
            contactTypeLUTID=1,
            participantID=1,
            staffID=1,
            physicianID=1,
            physicianPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        )
        contact4 = models.Contact(
            contactTypeLUTID=1,
            participantID=1,
            staffID=1,
            patientPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        )
        ctcFacility = models.CTCFacility(
            ctcID=1,
            facilityID=1,
            coc=123
        )
        incentive = models.Incentive(
            participantID=1,
            incentiveDescription="desc",
            barcode="123456789",
            dateGiven=datetime(2016, 4, 3)
        )
        db.session.add_all(ucrRoles)
        db.session.add_all(informantRelationships)
        db.session.add_all(users)
        db.session.add_all(states)
        db.session.add_all(finalCodes)
        db.session.add_all(sexes)
        db.session.add_all(abstractStatuses)
        db.session.add_all(races)
        db.session.add_all(ethnicities)
        db.session.add_all(vitals)
        db.session.add_all(contacts)
        db.session.add_all(inactives)
        db.session.add_all(ucrReportTypes)
        db.session.add_all(physicianStatuses)
        db.session.add_all(physFacilityStatuses)
        db.session.add_all(phoneTypes)
        db.session.add_all(irbHolders)
        db.session.add_all(projectTypes)
        db.session.add_all(contactStatuses)
        db.session.add_all(contactSources)
        db.session.add_all(grantStatuses)
        db.session.add_all(fundingSources)
        db.session.add_all(reviewCommitteeStatuses)
        db.session.add_all(projectStatuses)
        db.session.add_all(logTypes)
        db.session.add_all(reviewCommittees)
        db.session.add_all(staffRoles)
        db.session.add_all(projectPhases)
        db.session.add_all(hsts)
        db.session.add_all(tracingSources)
        db.session.add_all(contactTypes)
        db.session.add_all(giftCards)
        db.session.add(staff)
        db.session.add(staff2)
        db.session.add(project1)
        db.session.add(project2)
        db.session.add(funding)
        db.session.add(budget1)
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
        db.session.add(patientPhone2)
        db.session.add(informant1)
        db.session.add(informant2)
        db.session.add(informantAddress)
        db.session.add(informantPhone)
        db.session.add(informantPhone2)
        db.session.add(ctc1)
        db.session.add(ctc2)
        db.session.add(projectPatient)
        db.session.add(projectPatient2)
        db.session.add(projStatus)
        db.session.add(tracing)
        db.session.add(physician)
        db.session.add(physician2)
        db.session.add(physicianAddress)
        db.session.add(physicianEmail)
        db.session.add(physicianPhone)
        db.session.add(physicianPhone2)
        db.session.add(physicianToCTC)
        db.session.add(facility1)
        db.session.add(facility2)
        db.session.add(facilityAddress)
        db.session.add(facilityPhone)
        db.session.add(facilityPhone2)
        db.session.add(patientProjectStatusType1)
        db.session.add(patientProjectStatusType2)
        db.session.add(patientProjectStatus)
        db.session.add(physicianFacility)
        db.session.add(contact)
        db.session.add(contact2)
        db.session.add(contact3)
        db.session.add(contact4)
        db.session.add(ctcFacility)
        db.session.add(incentive)
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

class TestAbstractStatuses(PopulatedDB):
    def test_get_abstract_status(self):
        response = self.client.get("/api/abstractstatuses/1/")
        self.assertEqual(response.json["abstractStatusID"], 1)
        self.assertEqual(response.json["abstractStatus"], "Pending")
        self.assertEqual(response.json["versionID"], 1)

    def test_get_abstract_statuses(self):
        response = self.client.get("/api/abstractstatuses/")
        self.assertEqual(response.json["abstractStatuses"][0]["abstractStatusID"], 1)
        self.assertEqual(response.json["abstractStatuses"][0]["abstractStatus"], "Pending")
        self.assertEqual(response.json["abstractStatuses"][0]["versionID"], 1)

    def test_update_abstract_status(self):
        response = self.client.put("/api/abstractstatuses/1/", data={
            "abstractStatus": "status2",
            "versionID": 1
        })
        self.assertEqual(response.json["abstractStatusID"], 1)
        self.assertEqual(response.json["abstractStatus"], "status2")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_abstract_status(self):
        # Add a new status and then delete it (won't have dependencies)
        response = self.client.post("/api/abstractstatuses/", data={
            "abstractStatus": "status"
        })
        response2 = self.client.delete("/api/abstractstatuses/{}/".format(response.json["abstractStatusID"]))
        self.assertEqual(response2.json["Success"], True)
        self.assertEqual(response2.json["Message"], "AbstractStatusID {} deleted".format(response.json["abstractStatusID"]))

    def test_delete_abstract_status2(self):
        # Try to delete a status that has dependencies
        response = self.client.delete("/api/abstractstatuses/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["arcReviews"][0]["linkage"], False)
        self.assertEqual(response.json["arcReviews"][0]["engaged"], True)
        self.assertEqual(response.json["arcReviews"][0]["nonPublicData"], True)

    def test_get_arc_review(self):
        response = self.client.get("/api/arcreviews/1/")
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
        self.assertEqual(response.json["linkage"], False)
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
            "linkage": "true",
            "contact" : "false",
            "engaged" : "false",
            "nonPublicData" : "false",
            "versionID" : 1
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
        self.assertEqual(response.json["linkage"], True)
        self.assertEqual(response.json["engaged"], False)
        self.assertEqual(response.json["nonPublicData"], False)
        self.assertEqual(response.json["versionID"], 2)

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
            "periodComment" : "comment Updated",
            "versionID" : 1,
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["numPeriods"], 2)
        self.assertEqual(response.json["periodStart"], "2016-02-03")
        self.assertEqual(response.json["periodEnd"], "2016-02-03")
        self.assertEqual(response.json["periodTotal"], 1.5)
        self.assertEqual(response.json["periodComment"], "comment Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_budget(self):
        response = self.client.delete("/api/budgets/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "BudgetID 1 deleted")

class TestContact(PopulatedDB):
    def test_get_contacts_informant(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json["Contacts"][0]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["Contacts"][0]["participantID"], 1)
        self.assertEqual(response.json["Contacts"][0]["staffID"], 1)
        self.assertEqual(response.json["Contacts"][0]["informantID"], 1)
        self.assertEqual(response.json["Contacts"][0]["informantPhoneID"], 1)
        self.assertEqual(response.json["Contacts"][0]["facilityID"], None)
        self.assertEqual(response.json["Contacts"][0]["facilityPhoneID"], None)
        self.assertEqual(response.json["Contacts"][0]["physicianID"], None)
        self.assertEqual(response.json["Contacts"][0]["physicianPhoneID"], None)
        self.assertEqual(response.json["Contacts"][0]["patientPhoneID"], None)
        self.assertEqual(response.json["Contacts"][0]["description"], "desc")
        self.assertEqual(response.json["Contacts"][0]["contactDate"], "2016-02-02")
        self.assertEqual(response.json["Contacts"][0]["initials"], "atp")
        self.assertEqual(response.json["Contacts"][0]["notes"], "notes")
        self.assertEqual(response.json["Contacts"][0]["versionID"], 1)

    def test_get_contacts_faci1lity(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json["Contacts"][1]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["Contacts"][1]["participantID"], 1)
        self.assertEqual(response.json["Contacts"][1]["staffID"], 1)
        self.assertEqual(response.json["Contacts"][1]["informantID"], None)
        self.assertEqual(response.json["Contacts"][1]["informantPhoneID"], None)
        self.assertEqual(response.json["Contacts"][1]["facilityID"], 1)
        self.assertEqual(response.json["Contacts"][1]["facilityPhoneID"], 1)
        self.assertEqual(response.json["Contacts"][1]["physicianID"], None)
        self.assertEqual(response.json["Contacts"][1]["physicianPhoneID"], None)
        self.assertEqual(response.json["Contacts"][1]["patientPhoneID"], None)
        self.assertEqual(response.json["Contacts"][1]["description"], "desc")
        self.assertEqual(response.json["Contacts"][1]["contactDate"], "2016-02-02")
        self.assertEqual(response.json["Contacts"][1]["initials"], "atp")
        self.assertEqual(response.json["Contacts"][1]["notes"], "notes")
        self.assertEqual(response.json["Contacts"][1]["versionID"], 1)

    def test_get_contacts_physician(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json["Contacts"][2]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["Contacts"][2]["participantID"], 1)
        self.assertEqual(response.json["Contacts"][2]["staffID"], 1)
        self.assertEqual(response.json["Contacts"][2]["informantID"], None)
        self.assertEqual(response.json["Contacts"][2]["informantPhoneID"], None)
        self.assertEqual(response.json["Contacts"][2]["facilityID"],None)
        self.assertEqual(response.json["Contacts"][2]["facilityPhoneID"], None)
        self.assertEqual(response.json["Contacts"][2]["physicianID"], 1)
        self.assertEqual(response.json["Contacts"][2]["physicianPhoneID"], 1)
        self.assertEqual(response.json["Contacts"][2]["patientPhoneID"], None)
        self.assertEqual(response.json["Contacts"][2]["description"], "desc")
        self.assertEqual(response.json["Contacts"][2]["contactDate"], "2016-02-02")
        self.assertEqual(response.json["Contacts"][2]["initials"], "atp")
        self.assertEqual(response.json["Contacts"][2]["notes"], "notes")
        self.assertEqual(response.json["Contacts"][2]["versionID"], 1)

    def test_get_contacts_patient(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json["Contacts"][3]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["Contacts"][3]["participantID"], 1)
        self.assertEqual(response.json["Contacts"][3]["staffID"], 1)
        self.assertEqual(response.json["Contacts"][3]["informantID"], None)
        self.assertEqual(response.json["Contacts"][3]["informantPhoneID"], None)
        self.assertEqual(response.json["Contacts"][3]["facilityID"],None)
        self.assertEqual(response.json["Contacts"][3]["facilityPhoneID"], None)
        self.assertEqual(response.json["Contacts"][3]["physicianID"], None)
        self.assertEqual(response.json["Contacts"][3]["physicianPhoneID"], None)
        self.assertEqual(response.json["Contacts"][3]["patientPhoneID"], 1)
        self.assertEqual(response.json["Contacts"][3]["description"], "desc")
        self.assertEqual(response.json["Contacts"][3]["contactDate"], "2016-02-02")
        self.assertEqual(response.json["Contacts"][3]["initials"], "atp")
        self.assertEqual(response.json["Contacts"][3]["notes"], "notes")
        self.assertEqual(response.json["Contacts"][3]["versionID"], 1)

    def test_get_contact(self):
        response = self.client.get("/api/contacts/4/")
        self.assertEqual(response.json["contactTypeLUTID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["informantID"], None)
        self.assertEqual(response.json["informantPhoneID"], None)
        self.assertEqual(response.json["facilityID"],None)
        self.assertEqual(response.json["facilityPhoneID"], None)
        self.assertEqual(response.json["physicianID"], None)
        self.assertEqual(response.json["physicianPhoneID"], None)
        self.assertEqual(response.json["patientPhoneID"], 1)
        self.assertEqual(response.json["description"], "desc")
        self.assertEqual(response.json["contactDate"], "2016-02-02")
        self.assertEqual(response.json["initials"], "atp")
        self.assertEqual(response.json["notes"], "notes")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_contact(self):
        response = self.client.put("/api/contacts/4/",data = {
            "contactTypeLUTID" : 2,
            "participantID" : 2,
            "staffID" : 2,
            "informantID" : 1,
            "informantPhoneID" : 1,
            "facilityID" : 1,
            "facilityPhoneID": 1,
            "physicianID" : 1,
            "physicianPhoneID": 1,
            "patientPhoneID": None,
            "description" : "desc Updated",
            "contactDate" : "2016-02-03",
            "initials" : "atp Updated",
            "notes" : "notes Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["contactID"], 4)
        self.assertEqual(response.json["contactTypeLUTID"], 2)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["patientPhoneID"], None)
        self.assertEqual(response.json["description"], "desc Updated")
        self.assertEqual(response.json["contactDate"], "2016-02-03")
        self.assertEqual(response.json["initials"], "atp Updated")
        self.assertEqual(response.json["notes"], "notes Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_update_contact2(self):
        # Checks that you can't link the wrong phone with the entity
        response = self.client.put("/api/contacts/4/", data={
            "contactTypeLUTID": 2,
            "participantID": 2,
            "staffID": 2,
            "informantID": 2,
            "informantPhoneID": 1,
            "facilityID": 2,
            "facilityPhoneID": 1,
            "physicianID": 2,
            "physicianPhoneID": 1,
            "patientPhoneID": 1,
            "description": "desc Updated",
            "contactDate": "2016-02-03",
            "initials": "atp Updated",
            "notes": "notes Updated",
            "versionID": 1
        })
        

    def test_delete_contact(self):
        response = self.client.delete("/api/contacts/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactID 1 deleted")

class TestContactType(PopulatedDB):
    def test_get_contact_types(self):
        response = self.client.get("/api/contacttypes/")
        self.assertEqual(response.json["ContactTypes"][0]["contactTypeID"], 1)
        self.assertEqual(response.json["ContactTypes"][0]["contactDefinition"], "Mailed 1st packet to patient (intro letter, survey, consent, med rcd. release)")
        self.assertEqual(response.json["ContactTypes"][0]["contactCode"], 100)
        self.assertEqual(response.json["ContactTypes"][0]["versionID"], 1)

    def test_get_contact_type(self):
        response = self.client.get("/api/contacttypes/1/")
        self.assertEqual(response.json["contactTypeID"], 1)
        self.assertEqual(response.json["contactDefinition"], "Mailed 1st packet to patient (intro letter, survey, consent, med rcd. release)")
        self.assertEqual(response.json["contactCode"], 100)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_contact_type(self):
        response = self.client.put("/api/contacttypes/1/",data = {
            "contactDefinition" : "def Updated",
            "contactCode": 199,
            "versionID" : 1
        })
        self.assertEqual(response.json["contactTypeID"], 1)
        self.assertEqual(response.json["contactDefinition"], "def Updated")
        self.assertEqual(response.json["contactCode"], 199)
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_contact_type(self):
        response = self.client.delete("/api/contacttypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactTypeID 2 deleted")

class TestContactInfoSource(PopulatedDB):
    def test_get_contact_info_sourcees(self):
        response = self.client.get("/api/contactinfosources/")
        self.assertEqual(response.json["ContactInfoSources"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["ContactInfoSources"][0]["contactInfoSource"], "UCR")
        self.assertEqual(response.json["ContactInfoSources"][0]["versionID"], 1)

    def test_get_contact_info_source(self):
        response = self.client.get("/api/contactinfosources/1/")
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["contactInfoSource"], "UCR")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_contact_info_source(self):
        response = self.client.put("/api/contactinfosources/1/",data = {
            "contactInfoSource" : "source Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["contactInfoSource"], "source Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_contact_info_source(self):
        response = self.client.delete("/api/contactinfosources/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactInfoSourceID 2 deleted")

    def test_delete_contact_info_source2(self):
        response = self.client.delete("/api/contactinfosources/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestContactInfoStatus(PopulatedDB):
    def test_get_contact_info_statuses(self):
        response = self.client.get("/api/contactinfostatuses/")
        self.assertEqual(response.json["ContactInfoStatuses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["ContactInfoStatuses"][0]["contactInfoStatus"], "Current")
        self.assertEqual(response.json["ContactInfoStatuses"][0]["versionID"], 1)

    def test_get_contact_info_status(self):
        response = self.client.get("/api/contactinfostatuses/1/")
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["contactInfoStatus"], "Current")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_contact_info_status(self):
        response = self.client.put("/api/contactinfostatuses/1/",data = {
            "contactInfoStatus" : "status Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["contactInfoStatus"], "status Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_contact_info_status(self):
        response = self.client.delete("/api/contactinfostatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactInfoStatusID 2 deleted")

    def test_delete_contact_info_status2(self):
        response = self.client.delete("/api/contactinfostatuses/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestCTC(PopulatedDB):
    def test_get_ctcs(self):
        response = self.client.get("/api/ctcs/")
        self.assertEqual(response.json["CTCs"][0]["ctcID"], 1)
        self.assertEqual(response.json["CTCs"][0]["participantID"], 1)
        self.assertEqual(response.json["CTCs"][0]["dxDateDay"], 2)
        self.assertEqual(response.json["CTCs"][0]["dxDateMonth"], 7)
        self.assertEqual(response.json["CTCs"][0]["dxDateYear"], 1988)
        self.assertEqual(response.json["CTCs"][0]["site"], "Site 2")
        self.assertEqual(response.json["CTCs"][0]["histology"], "histology")
        self.assertEqual(response.json["CTCs"][0]["behavior"], "behavior")
        self.assertEqual(response.json["CTCs"][0]["ctcSequence"], "sequence")
        self.assertEqual(response.json["CTCs"][0]["stage"], "stage")
        self.assertEqual(response.json["CTCs"][0]["dxAge"], 1)
        self.assertEqual(response.json["CTCs"][0]["dxStreet1"], "street1")
        self.assertEqual(response.json["CTCs"][0]["dxStreet2"], "street2")
        self.assertEqual(response.json["CTCs"][0]["dxCity"], "city")
        self.assertEqual(response.json["CTCs"][0]["dxStateID"], 1)
        self.assertEqual(response.json["CTCs"][0]["dxZip"], "99999")
        self.assertEqual(response.json["CTCs"][0]["dxCounty"], "county")
        self.assertEqual(response.json["CTCs"][0]["dnc"], "dnc")
        self.assertEqual(response.json["CTCs"][0]["dncReason"], "dnc_reason")
        self.assertEqual(response.json["CTCs"][0]["recordID"], "abc321")

    def test_get_ctc(self):
        response = self.client.get("/api/ctcs/1/")
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["dxDateDay"], 2)
        self.assertEqual(response.json["dxDateMonth"], 7)
        self.assertEqual(response.json["dxDateYear"], 1988)
        self.assertEqual(response.json["site"], "Site 2")
        self.assertEqual(response.json["histology"], "histology")
        self.assertEqual(response.json["behavior"], "behavior")
        self.assertEqual(response.json["ctcSequence"], "sequence")
        self.assertEqual(response.json["stage"], "stage")
        self.assertEqual(response.json["dxAge"], 1)
        self.assertEqual(response.json["dxStreet1"], "street1")
        self.assertEqual(response.json["dxStreet2"], "street2")
        self.assertEqual(response.json["dxCity"], "city")
        self.assertEqual(response.json["dxStateID"], 1)
        self.assertEqual(response.json["dxZip"], "99999")
        self.assertEqual(response.json["dxCounty"], "county")
        self.assertEqual(response.json["dnc"], "dnc")
        self.assertEqual(response.json["dncReason"], "dnc_reason")
        self.assertEqual(response.json["recordID"], "abc321")

    def test_update_ctc(self):
        response = self.client.put("/api/ctcs/1/",data = {
            "participantID" : 2,
            "dxDateDay" : 3,
            "dxDateMonth" : 8,
            "dxDateYear" : 1990,
            "site" : "Site 1",
            "histology" : "histology2",
            "behavior" : "behavior2",
            "ctcSequence" : "sequence2",
            "stage" : "stage2",
            "dxAge" : 2,
            "dxStreet1" : "street12",
            "dxStreet2" : "street22",
            "dxCity" : "city2",
            "dxStateID" : 2,
            "dxZip" : "99991",
            "dxCounty" : "county2",
            "dnc" : "dnc2",
            "dncReason" : "dnc_reason2",
            "recordID" : "abc123",
            "versionID" : 1
        })
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["dxDateDay"], 3)
        self.assertEqual(response.json["dxDateMonth"], 8)
        self.assertEqual(response.json["dxDateYear"], 1990)
        self.assertEqual(response.json["site"], "Site 1")
        self.assertEqual(response.json["histology"], "histology2")
        self.assertEqual(response.json["behavior"], "behavior2")
        self.assertEqual(response.json["ctcSequence"], "sequence2")
        self.assertEqual(response.json["stage"], "stage2")
        self.assertEqual(response.json["dxAge"], 2)
        self.assertEqual(response.json["dxStreet1"], "street12")
        self.assertEqual(response.json["dxStreet2"], "street22")
        self.assertEqual(response.json["dxCity"], "city2")
        self.assertEqual(response.json["dxStateID"], 2)
        self.assertEqual(response.json["dxZip"], "99991")
        self.assertEqual(response.json["dxCounty"], "county2")
        self.assertEqual(response.json["dnc"], "dnc2")
        self.assertEqual(response.json["dncReason"], "dnc_reason2")
        self.assertEqual(response.json["recordID"], "abc123")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_ctc(self):
        response = self.client.delete("/api/ctcs/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "CtcID 2 deleted")

    def test_delete_ctc2(self):
        response = self.client.delete("/api/ctcs/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestCTCFacility(PopulatedDB):
    def test_get_ctc_facilities(self):
        response = self.client.get("/api/ctcfacilities/")
        self.assertEqual(response.json["CTCFacilities"][0]["CTCFacilityID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["ctcID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["facilityID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["coc"], 123)
        self.assertEqual(response.json["CTCFacilities"][0]["versionID"], 1)

    def test_get_ctc_facility(self):
        response = self.client.get("/api/ctcfacilities/1/")
        self.assertEqual(response.json["CTCFacilityID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["coc"], 123)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_ctc_facility(self):
        response = self.client.put("/api/ctcfacilities/1/",data = {
            "ctcID" : 2,
            "facilityID" : 2,
            "coc": 321,
            "versionID" : 1
        })
        self.assertEqual(response.json["CTCFacilityID"], 1)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["coc"], 321)
        self.assertEqual(response.json["versionID"], 2)

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
        self.assertEqual(response.json["FacilityPhones"][0]["phoneTypeID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["FacilityPhones"][0]["phoneStatusDate"], "2016-02-02")
        self.assertEqual(response.json["FacilityPhones"][0]["versionID"], 1)

    def test_get_facility_phone(self):
        response = self.client.get("/api/facilityphones/1/")
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["clinicName"], "clinic")
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_facility_phone(self):
        response = self.client.put("/api/facilityphones/1/", data = {
            "contactInfoSourceID" : 2,
            "facilityID" : 2,
            "contactInfoStatusID" : 2,
            "facilityName" : "name Updated",
            "clinicName" : "clinic Updated",
            "phoneTypeID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["clinicName"], "clinic Updated")
        self.assertEqual(response.json["phoneTypeID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_facility_phone(self):
        response = self.client.delete("/api/facilityphones/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityPhoneID 2 deleted")

    def test_delete_facility_phone2(self):
        response = self.client.delete("/api/facilityphones/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["Facilities"][0]["versionID"], 1)

    def test_get_facility(self):
        response = self.client.get("/api/facilities/1/")
        self.assertEqual(response.json["facilityName"], "name")
        self.assertEqual(response.json["contactFirstName"], "fname")
        self.assertEqual(response.json["contactLastName"], "lname")
        self.assertEqual(response.json["facilityStatus"], 1)
        self.assertEqual(response.json["facilityStatusDate"], "2016-02-02")
        self.assertEqual(response.json["contact2FirstName"], "fname")
        self.assertEqual(response.json["contact2LastName"], "lname")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_facility(self):
        response = self.client.put("/api/facilities/1/", data = {
            "facilityName" : "name2",
            "contactFirstName" : "fname2",
            "contactLastName" : "lname2",
            "facilityStatus" : 2,
            "facilityStatusDate" : "2016-02-03",
            "contact2FirstName" : "fname2",
            "contact2LastName" : "lname2",
            "versionID" : 1
        })
        self.assertEqual(response.json["facilityName"], "name2")
        self.assertEqual(response.json["contactFirstName"], "fname2")
        self.assertEqual(response.json["contactLastName"], "lname2")
        self.assertEqual(response.json["facilityStatus"], 2)
        self.assertEqual(response.json["facilityStatusDate"], "2016-02-03")
        self.assertEqual(response.json["contact2FirstName"], "fname2")
        self.assertEqual(response.json["contact2LastName"], "lname2")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_facility(self):
        response = self.client.delete("/api/facilities/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityID 2 deleted")

    def test_delete_facility2(self):
        response = self.client.delete("/api/facilities/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["FacilityAddresses"][0]["stateID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["zip"], "12345")
        self.assertEqual(response.json["FacilityAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["FacilityAddresses"][0]["versionID"], 1)

    def test_get_facility_address(self):
        response = self.client.get("/api/facilityaddresses/1/")
        self.assertEqual(response.json["facilityAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["stateID"], 1)
        self.assertEqual(response.json["zip"], "12345")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_facility_address(self):
        response = self.client.put("/api/facilityaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "facilityID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "stateID" : 2,
            "zip" : "zip Updated",
            "addressStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["facilityAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["stateID"], 2)
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_facility_address(self):
        response = self.client.delete("/api/facilityaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityAddressID 1 deleted")

class TestFinalCode(PopulatedDB):
    def test_get_final_codes(self):
        response = self.client.get("/api/finalcodes/")
        self.assertEqual(response.json["FinalCodes"][0]["finalCodeID"],1)
        self.assertEqual(response.json["FinalCodes"][0]["finalCodeDefinition"],"Pending")
        self.assertEqual(response.json["FinalCodes"][0]["finalCode"],0)
        self.assertEqual(response.json["FinalCodes"][0]["versionID"],1)

    def test_get_final_code(self):
        response = self.client.get("/api/finalcodes/1/")
        self.assertEqual(response.json["finalCodeID"], 1)
        self.assertEqual(response.json["finalCodeDefinition"], "Pending")
        self.assertEqual(response.json["finalCode"], 0)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_final_code(self):
        response = self.client.put("/api/finalcodes/1/", data={
            "finalCodeDefinition": "Pending Update",
            "finalCode": 1,
            "versionID": 1
        })
        self.assertEqual(response.json["finalCodeID"], 1)
        self.assertEqual(response.json["finalCodeDefinition"], "Pending Update")
        self.assertEqual(response.json["finalCode"], 1)
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_final_code(self):
        response = self.client.delete("/api/finalcodes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FinalCodeID 2 deleted")

    def test_delete_final_code2(self):
        response = self.client.delete("/api/finalcodes/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["Fundings"][0]["versionID"], 1)

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
        self.assertEqual(response.json["versionID"], 1)

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
            "secondaryChartfield": "scf Updated",
            "versionID" :1
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
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_funding(self):
        response = self.client.delete("/api/fundings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingID 1 deleted")

class TestFundingSource(PopulatedDB):
    def test_get_funding_sources(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json["FundingSources"][0]["fundingSourceID"], 1)
        self.assertEqual(response.json["FundingSources"][0]["fundingSource"], "NCI")

    def test_get_funding_source(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json["fundingSourceID"], 1)
        self.assertEqual(response.json["fundingSource"], "NCI")

    def test_update_funding_source(self):
        response = self.client.put("/api/fundingsources/1/", data = {
            "fundingSource" : "source2",
            "versionID" : 1
        })
        self.assertEqual(response.json["fundingSource"], "source2")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_funding_source(self):
        response = self.client.delete("/api/fundingsources/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingSourceID 2 deleted")

    def test_delete_funding_source2(self):
        response = self.client.delete("/api/fundingsources/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestGrantStatus(PopulatedDB):
    def test_get_grant_statuses(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json["GrantStatuses"][0]["grantStatusID"], 1)
        self.assertEqual(response.json["GrantStatuses"][0]["grantStatus"], "Submitted")
        self.assertEqual(response.json["GrantStatuses"][0]["versionID"], 1)

    def test_get_grant_status(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json["grantStatusID"], 1)
        self.assertEqual(response.json["grantStatus"], "Submitted")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_grant_status(self):
        response = self.client.put("/api/grantstatuses/1/", data = {
            "grantStatus" : "status2",
            "versionID" : 1
        })
        self.assertEqual(response.json["grantStatus"], "status2")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_grant_status(self):
        response = self.client.delete("/api/grantstatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "GrantStatusID 2 deleted")

    def test_delete_grant_status2(self):
        response = self.client.delete("/api/grantstatuses/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestHumanSubjectTraining(PopulatedDB):
    def test_get_human_subject_trainings(self):
        response = self.client.get("/api/humansubjecttrainings/")
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["trainingType"], "CITI")
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["versionID"], 1)

    def test_get_human_subject_training(self):
        response = self.client.get("/api/humansubjecttrainings/1/")
        self.assertEqual(response.json["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["trainingType"], "CITI")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_human_subject_training(self):
        response = self.client.put("/api/humansubjecttrainings/1/", data = {
            "trainingType" : "type Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["trainingType"], "type Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_human_subject_training(self):
        response = self.client.delete("/api/humansubjecttrainings/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "HumanSubjectTrainingID 2 deleted")

    def test_delete_human_subject_training2(self):
        response = self.client.delete("/api/humansubjecttrainings/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestIncentive(PopulatedDB):
    def test_get_incentives(self):
        response = self.client.get("/api/incentives/")
        self.assertEqual(response.json["Incentives"][0]["participantID"],1)
        self.assertEqual(response.json["Incentives"][0]["incentiveDescription"],"desc")
        self.assertEqual(response.json["Incentives"][0]["barcode"],"123456789")
        self.assertEqual(response.json["Incentives"][0]["dateGiven"],"2016-04-03")
        self.assertEqual(response.json["Incentives"][0]["versionID"],1)

    def test_get_incentive(self):
        response = self.client.get("/api/incentives/1/")
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["incentiveDescription"],"desc")
        self.assertEqual(response.json["barcode"],"123456789")
        self.assertEqual(response.json["dateGiven"],"2016-04-03")
        self.assertEqual(response.json["versionID"],1)

    def test_update_incentive(self):
        response = self.client.put("/api/incentives/1/", data = {
            "participantID" : 2,
            "incentiveDescription" : "desc Updated",
            "dateGiven" : "2016-02-03",
            "barcode" : "123456788",
            "versionID" : 1
        })
        self.assertEqual(response.json["participantID"],2)
        self.assertEqual(response.json["incentiveDescription"],"desc Updated")
        self.assertEqual(response.json["dateGiven"],"2016-02-03")
        self.assertEqual(response.json["barcode"],"123456788")
        self.assertEqual(response.json["versionID"],2)

    def test_update_incentive2(self):
        response = self.client.put("/api/incentives/1/", data={
            "participantID": 2,
            "incentiveDescription": "desc Updated",
            "dateGiven": "2016-02-03",
            "barcode": "987654321",
            "versionID": 1
        })
        self.assertEqual(response.json, {'Error': "{'barcode': ['Barcode not found in gift card table.']}"})

    def test_delete_incentive(self):
        response = self.client.delete("/api/incentives/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "IncentiveID 1 deleted")

class TestInformant(PopulatedDB):
    def test_get_informants(self):
        response = self.client.get("/api/informants/")
        self.assertEqual(response.json["Informants"][0]["informantID"], 1)
        self.assertEqual(response.json["Informants"][0]["participantID"], 1)
        self.assertEqual(response.json["Informants"][0]["firstName"], "fname")
        self.assertEqual(response.json["Informants"][0]["lastName"], "lname")
        self.assertEqual(response.json["Informants"][0]["middleName"], "middle_name")
        self.assertEqual(response.json["Informants"][0]["informantPrimary"], True)
        self.assertEqual(response.json["Informants"][0]["informantRelationshipID"], 1)
        self.assertEqual(response.json["Informants"][0]["notes"], "notes")
        self.assertEqual(response.json["Informants"][0]["versionID"], 1)

    def test_get_informant(self):
        response = self.client.get("/api/informants/1/")
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["middleName"], "middle_name")
        self.assertEqual(response.json["informantPrimary"], True)
        self.assertEqual(response.json["informantRelationshipID"], 1),
        self.assertEqual(response.json["notes"], "notes")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_informant(self):
        response = self.client.put("/api/informants/1/", data = {
            "participantID" : 2,
            "firstName" : "fname Updated",
            "lastName" : "lname Updated",
            "middleName" : "middle_name Updated",
            "informantPrimary" : "false",
            "informantRelationshipID" : 2,
            "notes" : "notes Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["firstName"], "fname Updated")
        self.assertEqual(response.json["lastName"], "lname Updated")
        self.assertEqual(response.json["middleName"], "middle_name Updated")
        self.assertEqual(response.json["informantPrimary"], False)
        self.assertEqual(response.json["informantRelationshipID"], 2)
        self.assertEqual(response.json["notes"], "notes Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_informant(self):
        response = self.client.delete("/api/informants/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantID 2 deleted")

    def test_delete_informant2(self):
        response = self.client.delete("/api/informants/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["InformantAddresses"][0]["stateID"], 2)
        self.assertEqual(response.json["InformantAddresses"][0]["zip"], "12345")
        self.assertEqual(response.json["InformantAddresses"][0]["addressStatusDate"], "2016-02-02")

    def test_get_informant_address(self):
        response = self.client.get("/api/informantaddresses/1/")
        self.assertEqual(response.json["informantAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["stateID"], 2)
        self.assertEqual(response.json["zip"], "12345")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")

    def test_update_informant_address(self):
        response = self.client.put("/api/informantaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "informantID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "stateID" : 1,
            "zip" : "zip Updated",
            "addressStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["informantAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["stateID"], 1)
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

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
        self.assertEqual(response.json["InformantPhones"][0]["phoneTypeID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["InformantPhones"][0]["phoneStatusDate"], "2016-02-02")
        self.assertEqual(response.json["InformantPhones"][0]["versionID"], 1)

    def test_get_informant_phone(self):
        response = self.client.get("/api/informantphones/1/")
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_informant_phone(self):
        response = self.client.put("/api/informantphones/1/", data = {
            "contactInfoSourceID" : 2,
            "informantID" : 2,
            "contactInfoStatusID" : 2,
            "phoneTypeID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phoneTypeID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_informant_phone(self):
        response = self.client.delete("/api/informantphones/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantPhoneID 2 deleted")

    def test_delete_informant_phone2(self):
        response = self.client.delete("/api/informantphones/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestIRBHolder(PopulatedDB):
    def test_get_irb_holders(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json["irbHolders"][0]["holder"],"U of U")
        self.assertEqual(response.json["irbHolders"][0]["holderDefinition"],"U of U researcher is responsible for IRB")
        self.assertEqual(response.json["irbHolders"][0]["versionID"],1)

    def test_get_irb_holder(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json["holder"],"U of U")
        self.assertEqual(response.json["holderDefinition"],"U of U researcher is responsible for IRB")
        self.assertEqual(response.json["versionID"],1)

    def test_update_irb_holder(self):
        response = self.client.put("/api/irbholders/1/", data = {
            "holder" : "holder 1 Updated",
            "holderDefinition" : "IRB 1 Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["holder"],"holder 1 Updated")
        self.assertEqual(response.json["holderDefinition"],"IRB 1 Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_irb_holder(self):
        response = self.client.delete("/api/irbholders/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "IrbHolderID 2 deleted")

    def test_delete_irb_holder2(self):
        response = self.client.delete("/api/irbholders/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestLog(PopulatedDB):
    def test_get_logs(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.json["Logs"][0]["logSubjectID"],1)
        self.assertEqual(response.json["Logs"][0]["projectID"],1)
        self.assertEqual(response.json["Logs"][0]["staffID"],1)
        self.assertEqual(response.json["Logs"][0]["phaseStatusID"],1)
        self.assertEqual(response.json["Logs"][0]["note"],"note")
        self.assertEqual(response.json["Logs"][0]["date"],"2016-02-02")
        self.assertEqual(response.json["Logs"][0]["versionID"],1)

    def test_get_log(self):
        response = self.client.get("/api/logs/1/")
        self.assertEqual(response.json["logSubjectID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["phaseStatusID"],1)
        self.assertEqual(response.json["note"],"note")
        self.assertEqual(response.json["date"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

    def test_update_log(self):
        response = self.client.put("/api/logs/1/", data = {
            "logSubjectID" : 2,
            "projectID" : 2,
            "staffID" : 2,
            "phaseStatusID" : 2,
            "note" : "note Updated",
            "date" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["logSubjectID"],2)
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["staffID"],2)
        self.assertEqual(response.json["phaseStatusID"],2)
        self.assertEqual(response.json["note"],"note Updated")
        self.assertEqual(response.json["date"],"2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_log(self):
        response = self.client.delete("/api/logs/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogID 1 deleted")

class TestLogSubject(PopulatedDB):
    def test_get_log_subjects(self):
        response = self.client.get("/api/logsubjects/")
        self.assertEqual(response.json["LogSubjects"][0]["logSubject"], "Review Committee")
        self.assertEqual(response.json["LogSubjects"][0]["versionID"], 1)

    def test_get_log_subject(self):
        response = self.client.get("/api/logsubjects/1/")
        self.assertEqual(response.json["logSubject"], "Review Committee")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_log_subject(self):
        response = self.client.put("/api/logsubjects/1/", data = {
            "logSubject" : "subject Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["logSubject"], "subject Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_log_subject(self):
        response = self.client.delete("/api/logsubjects/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogSubjectID 2 deleted")

    def test_delete_log_subject2(self):
        response = self.client.delete("/api/logsubjects/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestPatient(PopulatedDB):
    def test_get_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json["Patients"][0]["patID"], "1")
        self.assertEqual(response.json["Patients"][0]["ucrDistID"], 1)
        self.assertEqual(response.json["Patients"][0]["UPDBID"], 1)
        self.assertEqual(response.json["Patients"][0]["firstName"], "fname")
        self.assertEqual(response.json["Patients"][0]["lastName"], "lname")
        self.assertEqual(response.json["Patients"][0]["maidenName"], "maiden_name")
        self.assertEqual(response.json["Patients"][0]["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["Patients"][0]["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["Patients"][0]["aliasMiddleName"], "alias_middle")
        self.assertEqual(response.json["Patients"][0]["dobDay"], 15)
        self.assertEqual(response.json["Patients"][0]["dobMonth"], 2)
        self.assertEqual(response.json["Patients"][0]["dobYear"], 1990)
        self.assertEqual(response.json["Patients"][0]["SSN"], "999999999")
        self.assertEqual(response.json["Patients"][0]["sexID"], 2)
        self.assertEqual(response.json["Patients"][0]["raceID"], 1)
        self.assertEqual(response.json["Patients"][0]["ethnicityID"], 1)
        self.assertEqual(response.json["Patients"][0]["vitalStatusID"], 1)
        self.assertEqual(response.json["Patients"][0]["versionID"], 1)

    def test_get_patient(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json["patID"], "1")
        self.assertEqual(response.json["ucrDistID"], 1)
        self.assertEqual(response.json["UPDBID"], 1)
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["maidenName"], "maiden_name")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle")
        self.assertEqual(response.json["dobDay"], 15)
        self.assertEqual(response.json["dobMonth"], 2)
        self.assertEqual(response.json["dobYear"], 1990)
        self.assertEqual(response.json["SSN"], "999999999")
        self.assertEqual(response.json["sexID"], 2)
        self.assertEqual(response.json["raceID"], 1)
        self.assertEqual(response.json["ethnicityID"], 1)
        self.assertEqual(response.json["vitalStatusID"], 1)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_patient(self):
        response = self.client.put("/api/patients/1/", data = {
            "patID" : "2",
            "ucrDistID" : 2,
            "UPDBID" : 2,
            "firstName" : "fname Updated",
            "lastName" : "lname Updated",
            "middleName" : "mname Updated",
            "maidenName" : "maiden_name Updated",
            "aliasFirstName" : "alias_fname Updated",
            "aliasLastName" : "alias_lname Updated",
            "aliasMiddleName" : "alias_middle Updated",
            "dobDay" : 1,
            "dobMonth" : 1,
            "dobYear" : 2000,
            "SSN" : "999999990",
            "sexID" : 1,
            "raceID" : 2,
            "ethnicityID" : 2,
            "vitalStatusID" : 2,
            "versionID" : 1
        })
        self.assertEqual(response.json["patID"], "2")
        self.assertEqual(response.json["ucrDistID"], 2)
        self.assertEqual(response.json["UPDBID"], 2)
        self.assertEqual(response.json["firstName"], "fname Updated")
        self.assertEqual(response.json["lastName"], "lname Updated")
        self.assertEqual(response.json["maidenName"], "maiden_name Updated")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname Updated")
        self.assertEqual(response.json["aliasLastName"], "alias_lname Updated")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle Updated")
        self.assertEqual(response.json["dobDay"], 1)
        self.assertEqual(response.json["dobMonth"], 1)
        self.assertEqual(response.json["dobYear"], 2000)
        self.assertEqual(response.json["SSN"], "999999990")
        self.assertEqual(response.json["sexID"], 1)
        self.assertEqual(response.json["raceID"], 2)
        self.assertEqual(response.json["ethnicityID"], 2)
        self.assertEqual(response.json["vitalStatusID"], 2)
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_patient(self):
        response = self.client.delete("/api/patients/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientID 2 deleted")

    def test_delete_patient2(self):
        response = self.client.delete("/api/patients/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestPatientAddress(PopulatedDB):
    def test_get_patient_addresses(self):
        response = self.client.get("/api/patientaddresses/")
        self.assertEqual(response.json["PatientAddresses"][0]["patAddressID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["participantID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["street"], "street")
        self.assertEqual(response.json["PatientAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["PatientAddresses"][0]["city"], "city")
        self.assertEqual(response.json["PatientAddresses"][0]["stateID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["zip"], "12345")
        self.assertEqual(response.json["PatientAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PatientAddresses"][0]["versionID"], 1)

    def test_get_patient_address(self):
        response = self.client.get("/api/patientaddresses/1/")
        self.assertEqual(response.json["patAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["stateID"], 1)
        self.assertEqual(response.json["zip"], "12345")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_patient_address(self):
        response = self.client.put("/api/patientaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "participantID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "stateID" : 2,
            "zip" : "zip Updated",
            "addressStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["patAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["stateID"], 2)
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_patient_address(self):
        response = self.client.delete("/api/patientaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatAddressID 1 deleted")

class TestPatientEmail(PopulatedDB):
    def test_get_patient_emails(self):
        response = self.client.get("/api/patientemails/")
        self.assertEqual(response.json["PatientEmails"][0]["emailID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["participantID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["email"], "email")
        self.assertEqual(response.json["PatientEmails"][0]["emailStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PatientEmails"][0]["versionID"], 1)

    def test_get_patient_email(self):
        response = self.client.get("/api/patientemails/1/")
        self.assertEqual(response.json["emailID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["email"], "email")
        self.assertEqual(response.json["emailStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_patient_email(self):
        response = self.client.put("/api/patientemails/1/", data = {
            "contactInfoSourceID" : 2,
            "participantID" : 2,
            "contactInfoStatusID" : 2,
            "email" : "email Updated",
            "emailStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["emailID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["email"], "email Updated")
        self.assertEqual(response.json["emailStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_patient_email(self):
        response = self.client.delete("/api/patientemails/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "EmailID 1 deleted")

class TestPatientPhone(PopulatedDB):
    def test_get_patient_phones(self):
        response = self.client.get("/api/patientphones/")
        self.assertEqual(response.json["PatientPhones"][0]["patPhoneID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["participantID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["phoneTypeID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["PatientPhones"][0]["versionID"], 1)

    def test_get_patient_phone(self):
        response = self.client.get("/api/patientphones/1/")
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_patient_phone(self):
        response = self.client.put("/api/patientphones/1/", data = {
            "contactInfoSourceID" : 2,
            "participantID" : 2,
            "contactInfoStatusID" : 2,
            "phoneTypeID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneTypeID"], 2)
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_patient_phone(self):
        response = self.client.delete("/api/patientphones/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatPhoneID 2 deleted")

    def test_delete_patient_phone2(self):
        response = self.client.delete("/api/patientphones/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestPatientProjectStatus(PopulatedDB):
    def test_get_patient_project_statuses(self):
        response = self.client.get("/api/patientprojectstatuses/")
        self.assertEqual(response.json["PatientProjectStatuses"][0]["patientProjectStatusID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["participantID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["statusDate"], "2016-02-02")
        self.assertEqual(response.json["PatientProjectStatuses"][0]["versionID"], 1)

    def test_get_patient_project_status(self):
        response = self.client.get("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json["patientProjectStatusID"], 1)
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["statusDate"], "2016-02-02")
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_patient_project_status(self):
        response = self.client.put("/api/patientprojectstatuses/1/", data = {
            "patientProjectStatusTypeID" : 2,
            "participantID" : 2,
            "statusDate": "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["patientProjectStatusID"], 1)
        self.assertEqual(response.json["patientProjectStatusTypeID"], 2)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["statusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_patient_project_status(self):
        response = self.client.delete("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientProjectStatusID 1 deleted")

class TestPatientProjectStatusLUT(PopulatedDB):
    def test_get_patient_project_status_types(self):
        response = self.client.get("/api/patientprojectstatustypes/")
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["statusDescription"], "desc")
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["versionID"], 1)

    def test_get_patient_project_status_type(self):
        response = self.client.get("/api/patientprojectstatustypes/1/")
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["statusDescription"], "desc")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_patient_project_status_type(self):
        response = self.client.put("/api/patientprojectstatustypes/1/", data = {
            "statusDescription" : "desc Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["statusDescription"], "desc Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_patient_project_status_type(self):
        response = self.client.delete("/api/patientprojectstatustypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientProjectStatusTypeID 2 deleted")

    def test_delete_patient_project_status_type2(self):
        response = self.client.delete("/api/patientprojectstatustypes/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestPhaseStatus(PopulatedDB):
    def test_get_phase_statuses(self):
        response = self.client.get("/api/phasestatuses/")
        self.assertEqual(response.json["PhaseStatuses"][0]["phaseStatus"], "Received")
        self.assertEqual(response.json["PhaseStatuses"][0]["phaseDescription"], "Items received from investigator")
        self.assertEqual(response.json["PhaseStatuses"][0]["versionID"], 1)

    def test_get_phase_status(self):
        response = self.client.get("/api/phasestatuses/1/")
        self.assertEqual(response.json["phaseStatus"], "Received")
        self.assertEqual(response.json["phaseDescription"], "Items received from investigator")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_phase_status(self):
        response = self.client.put("/api/phasestatuses/1/", data = {
            "phaseStatus" : "status Updated",
            "phaseDescription": "desc Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["phaseStatus"], "status Updated")
        self.assertEqual(response.json["phaseDescription"], "desc Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_phase_status(self):
        response = self.client.delete("/api/phasestatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogPhaseID 2 deleted")

    def test_delete_phase_status2(self):
        response = self.client.delete("/api/phasestatuses/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestPhoneType(PopulatedDB):
    def test_get_phone_types(self):
        response = self.client.get("/api/phonetypes/")
        self.assertEqual(response.json["PhoneTypes"][0]["phoneTypeID"], 1)
        self.assertEqual(response.json["PhoneTypes"][0]["phoneType"], "cell")

    def test_get_phone_type(self):
        response = self.client.get("/api/phonetypes/1/")
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneType"], "cell")

    def test_update_phone_type(self):
        response = self.client.put("/api/phonetypes/1/", data = {
            "phoneType" : "home",
            "versionID" : 1
        })
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneType"], "home")

    def test_delete_phone_type(self):
        response = self.client.delete("/api/phonetypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhoneTypeID 2 deleted")

    def test_delete_phone_type2(self):
        response = self.client.delete("/api/phonetypes/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["Physicians"][0]["physicianStatusID"], 1)
        self.assertEqual(response.json["Physicians"][0]["physicianStatusDate"], "2016-02-02")
        self.assertEqual(response.json["Physicians"][0]["versionID"], 1)

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
        self.assertEqual(response.json["physicianStatusID"], 1)
        self.assertEqual(response.json["physicianStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

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
            "physicianStatusID" : 2,
            "physicianStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["firstName"], "fname2")
        self.assertEqual(response.json["lastName"], "lname2")
        self.assertEqual(response.json["middleName"], "middle_name2")
        self.assertEqual(response.json["credentials"], "credentials2")
        self.assertEqual(response.json["specialty"], "specialty2")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname2")
        self.assertEqual(response.json["aliasLastName"], "alias_lname2")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle_name2")
        self.assertEqual(response.json["physicianStatusID"], 2)
        self.assertEqual(response.json["physicianStatusDate"], "2016-02-03")

    def test_delete_physician(self):
        response = self.client.delete("/api/physicians/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianID 2 deleted")

    def test_delete_physician2(self):
        response = self.client.delete("/api/physicians/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["PhysicianAddresses"][0]["stateID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["zip"], "12345")
        self.assertEqual(response.json["PhysicianAddresses"][0]["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PhysicianAddresses"][0]["versionID"], 1)

    def test_get_physician_address(self):
        response = self.client.get("/api/physicianaddresses/1/")
        self.assertEqual(response.json["physicianAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["stateID"], 1)
        self.assertEqual(response.json["zip"], "12345")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_physician_address(self):
        response = self.client.put("/api/physicianaddresses/1/", data = {
            "contactInfoSourceID" : 2,
            "physicianID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "stateID" : 2,
            "zip" : "zip Updated",
            "addressStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["physicianAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["stateID"], 2)
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["addressStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_physician_address(self):
        response = self.client.delete("/api/physicianaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianAddressID 1 deleted")

class TestPhysicianEmail(PopulatedDB):
    def test_get_physician_emails(self):
        response = self.client.get("/api/physicianemails/")
        self.assertEqual(response.json["PhysicianEmails"][0]["physicianEmailID"], 1)
        self.assertEqual(response.json["PhysicianEmails"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PhysicianEmails"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianEmails"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PhysicianEmails"][0]["email"], "email")
        self.assertEqual(response.json["PhysicianEmails"][0]["emailStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PhysicianEmails"][0]["versionID"], 1)

    def test_get_physician_email(self):
        response = self.client.get("/api/physicianemails/1/")
        self.assertEqual(response.json["physicianEmailID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["email"], "email")
        self.assertEqual(response.json["emailStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_physician_email(self):
        response = self.client.put("/api/physicianemails/1/", data = {
            "contactInfoSourceID" : 2,
            "physicianID" : 2,
            "contactInfoStatusID" : 2,
            "email" : "email Updated",
            "emailStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["physicianEmailID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["email"], "email Updated")
        self.assertEqual(response.json["emailStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_physician_email(self):
        response = self.client.delete("/api/physicianemails/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianEmailID 1 deleted")

class TestPhysicianFacility(PopulatedDB):
    def test_get_physician_facilities(self):
        response = self.client.get("/api/physicianfacilities/")
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["facilityID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityStatusID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityStatusDate"], "2016-02-02")
        self.assertEqual(response.json["PhysicianFacilities"][0]["versionID"], 1)

    def test_get_physician_facility(self):
        response = self.client.get("/api/physicianfacilities/1/")
        self.assertEqual(response.json["physFacilityID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["physFacilityStatusID"], 1)
        self.assertEqual(response.json["physFacilityStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_physician_facility(self):
        response = self.client.put("/api/physicianfacilities/1/", data = {
            "facilityID" : 2,
            "physicianID" : 2,
            "physFacilityStatusID" : 2,
            "physFacilityStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["physFacilityID"], 1)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["physFacilityStatusID"], 2)
        self.assertEqual(response.json["physFacilityStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_physician_facility(self):
        response = self.client.delete("/api/physicianfacilities/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysFacilityID 1 deleted")

class TestPhysicianPhone(PopulatedDB):
    def test_get_physician_phones(self):
        response = self.client.get("/api/physicianphones/")
        self.assertEqual(response.json["PhysicianPhones"][0]["physicianPhoneID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["contactInfoSourceID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneTypeID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["phoneStatusDate"], "2016-02-02")

    def test_get_physician_phone(self):
        response = self.client.get("/api/physicianphones/1/")
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")

    def test_update_physician_phone(self):
        response = self.client.put("/api/physicianphones/1/", data = {
            "contactInfoSourceID" : 2,
            "physicianID" : 2,
            "contactInfoStatusID" : 2,
            "phoneNumber" : "phone Updated",
            "phoneTypeID": 2,
            "phoneStatusDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phoneNumber"], "phone Updated")
        self.assertEqual(response.json["phoneTypeID"], 2)
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_physician_phone(self):
        response = self.client.delete("/api/physicianphones/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianPhoneID 2 deleted")

    def test_delete_physician_phone2(self):
        response = self.client.delete("/api/physicianphones/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestPhysicianToCTC(PopulatedDB):
    def test_get_physician_to_ctcs(self):
        response = self.client.get("/api/physiciantoctcs/")
        self.assertEqual(response.json["PhysicianToCTCs"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianToCTCs"][0]["ctcID"], 1)
        self.assertEqual(response.json["PhysicianToCTCs"][0]["versionID"], 1)

    def test_get_physician_to_ctc(self):
        response = self.client.get("/api/physiciantoctcs/1/")
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_physician_to_ctc(self):
        response = self.client.put("/api/physiciantoctcs/1/", data = {
            "physicianID" : 2,
            "ctcID": 2,
            "versionID" : 1
        })
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["versionID"], 2)

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
            "irb0" : "false",
            "irb1" : "false",
            "irb2" : "false",
            "irb3" : "false",
            "irb4" : "false",
            "otherIrb" : "other_irb2",
            "updb" : "false",
            "ptContact" : "false",
            "startDate" : "2016-02-03",
            "link" : "false",
            "deliveryDate" : "2016-02-03",
            "description" : "description2",
            "versionID" : 1
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
        self.assertEqual(response.json["versionID"], 2)

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
        self.assertEqual(response.json["projects"][0]["projectTitle"],"Test Project")
        self.assertEqual(response.json["projects"][0]["shortTitle"],"Test Project")
        self.assertEqual(response.json["projects"][0]["projectSummary"],"Summary")
        self.assertEqual(response.json["projects"][0]["sop"],"sop")
        self.assertEqual(response.json["projects"][0]["ucrProposal"],"ucr_proposal")
        self.assertEqual(response.json["projects"][0]["budgetDoc"],"budget_doc")
        self.assertEqual(response.json["projects"][0]["ucrFee"],"no")
        self.assertEqual(response.json["projects"][0]["ucrNoFee"],"yes")
        self.assertEqual(response.json["projects"][0]["previousShortTitle"],"t short")
        self.assertEqual(response.json["projects"][0]["dateAdded"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["finalRecruitmentReport"],"report")
        self.assertEqual(response.json["projects"][0]["ongoingContact"],True)
        self.assertEqual(response.json["projects"][0]["activityStartDate"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["activityEndDate"],"2016-02-02")
    # Test getting single project
    def test_get_project(self):
        response = self.client.get("/api/projects/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectTypeID"],1)
        self.assertEqual(response.json["irbHolderID"],1)
        self.assertEqual(response.json["projectTitle"],"Test Project")
        self.assertEqual(response.json["shortTitle"],"Test Project")
        self.assertEqual(response.json["projectSummary"],"Summary")
        self.assertEqual(response.json["sop"],"sop")
        self.assertEqual(response.json["ucrProposal"],"ucr_proposal")
        self.assertEqual(response.json["budgetDoc"],"budget_doc")
        self.assertEqual(response.json["ucrFee"],"no")
        self.assertEqual(response.json["ucrNoFee"],"yes")
        self.assertEqual(response.json["previousShortTitle"],"t short")
        self.assertEqual(response.json["dateAdded"],"2016-02-02")
        self.assertEqual(response.json["finalRecruitmentReport"],"report")
        self.assertEqual(response.json["ongoingContact"],True)
        self.assertEqual(response.json["activityStartDate"],"2016-02-02")
        self.assertEqual(response.json["activityEndDate"],"2016-02-02")

    # Test update project
    def test_update_project(self):
        response = self.client.put("/api/projects/1/",data = {
            "projectTypeID" : 2,
            "irbHolderID" : 2,
            "projectTitle" : "Test Project Update",
            "shortTitle" : "Test Project Update",
            "projectSummary" : "Summary Update",
            "sop":"sop Update",
            "ucrProposal":"ucr_proposal Update",
            "budgetDoc" : "budget_doc Update",
            "ucrFee" : "no Update",
            "ucrNoFee" : "yes Update",
            "previousShortTitle" : "t short Update",
            "dateAdded" : "2016-02-03",
            "finalRecruitmentReport" : "report Update",
            "ongoingContact" : "false",
            "activityStartDate" : "2016-02-03",
            "activityEndDate" : "2016-02-03",
            "versionID" : 1
        })
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectTypeID"],2)
        self.assertEqual(response.json["irbHolderID"],2)
        self.assertEqual(response.json["projectTitle"],"Test Project Update")
        self.assertEqual(response.json["shortTitle"],"Test Project Update")
        self.assertEqual(response.json["projectSummary"],"Summary Update")
        self.assertEqual(response.json["sop"],"sop Update")
        self.assertEqual(response.json["ucrProposal"],"ucr_proposal Update")
        self.assertEqual(response.json["budgetDoc"],"budget_doc Update")
        self.assertEqual(response.json["ucrFee"],"no Update")
        self.assertEqual(response.json["ucrNoFee"],"yes Update")
        self.assertEqual(response.json["previousShortTitle"],"t short Update")
        self.assertEqual(response.json["dateAdded"],"2016-02-03")
        self.assertEqual(response.json["finalRecruitmentReport"],"report Update")
        self.assertEqual(response.json["ongoingContact"],False)
        self.assertEqual(response.json["activityStartDate"],"2016-02-03")
        self.assertEqual(response.json["activityEndDate"],"2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

     # Test deletetion of project
    def test_delete_project(self):
        response = self.client.delete("/api/projects/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectID 2 deleted")

    def test_delete_project2(self):
        response = self.client.delete("/api/projects/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

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
        self.assertEqual(response.json["ProjectPatients"][0]["finalCodeID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["finalCodeDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["enrollmentDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["dateCoordSigned"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["importDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["finalCodeStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["enrollmentStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["dateCoordSignedStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstractStatusID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstractStatusDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractStatusStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["sentToAbstractorDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["sentToAbstractorStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstractedDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractorStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["researcherDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["researcherStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["consentLink"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseSigned"], True)
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseLink"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["medRecordReleaseDate"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["surveyToResearcher"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["surveyToResearcherStaffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["qualityControl"], True)
        self.assertEqual(response.json["ProjectPatients"][0]["versionID"], 1)

    def test_get_project_patient(self):
        response = self.client.get("/api/projectpatients/1/")
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["currentAge"], 1)
        self.assertEqual(response.json["batch"], 1)
        self.assertEqual(response.json["siteGrp"], 1)
        self.assertEqual(response.json["finalCodeID"], 1)
        self.assertEqual(response.json["finalCodeDate"], "2016-02-02")
        self.assertEqual(response.json["enrollmentDate"], "2016-02-02")
        self.assertEqual(response.json["dateCoordSigned"], "2016-02-02")
        self.assertEqual(response.json["importDate"], "2016-02-02")
        self.assertEqual(response.json["finalCodeStaffID"], 1)
        self.assertEqual(response.json["enrollmentStaffID"], 1)
        self.assertEqual(response.json["dateCoordSignedStaffID"],1)
        self.assertEqual(response.json["abstractStatusID"], 1)
        self.assertEqual(response.json["abstractStatusDate"], "2016-02-02")
        self.assertEqual(response.json["abstractStatusStaffID"], 1)
        self.assertEqual(response.json["sentToAbstractorDate"], "2016-02-02")
        self.assertEqual(response.json["sentToAbstractorStaffID"], 1)
        self.assertEqual(response.json["abstractedDate"], "2016-02-02")
        self.assertEqual(response.json["abstractorStaffID"], 1)
        self.assertEqual(response.json["researcherDate"], "2016-02-02")
        self.assertEqual(response.json["researcherStaffID"], 1)
        self.assertEqual(response.json["consentLink"], "link")
        self.assertEqual(response.json["medRecordReleaseSigned"], True)
        self.assertEqual(response.json["medRecordReleaseLink"], "link")
        self.assertEqual(response.json["medRecordReleaseStaffID"], 1)
        self.assertEqual(response.json["medRecordReleaseDate"], "2016-02-02")
        self.assertEqual(response.json["surveyToResearcher"], "2016-02-02")
        self.assertEqual(response.json["surveyToResearcherStaffID"], 1)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_project_patient(self):
        response = self.client.put("/api/projectpatients/1/", data = {
            "projectID" : 2,
            "staffID" : 2,
            "ctcID" : 2,
            "currentAge" : 2,
            "batch"  : 2,
            "siteGrp" : 2,
            "finalCodeID" : 2,
            "finalCodeDate" : "2016-02-03",
            "enrollmentDate" : "2016-02-03",
            "dateCoordSigned" : "2016-02-03",
            "importDate" : "2016-02-03",
            "finalCodeStaffID" : 2,
            "enrollmentStaffID" : 2,
            "dateCoordSignedStaffID"  :2,
            "abstractStatusID" : 2,
            "abstractStatusDate" : "2016-02-03",
            "abstractStatusStaffID" : 2,
            "sentToAbstractorDate"  : "2016-02-03",
            "sentToAbstractorStaffID" : 2,
            "abstractedDate" : "2016-02-03",
            "abstractorStaffID" : 2,
            "researcherDate" : "2016-02-03",
            "researcherStaffID" : 2,
            "consentLink" : "link Updated",
            "tracingStatus" : 2,
            "medRecordReleaseSigned" : "false",
            "medRecordReleaseLink" : "link Updated",
            "medRecordReleaseStaffID" : 2,
            "medRecordReleaseDate"  : "2016-02-03",
            "surveyToResearcher"  : "2016-02-03",
            "surveyToResearcherStaffID" : 2,
            "qualityControl": "false",
            "versionID" : 1
        })
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["currentAge"], 2)
        self.assertEqual(response.json["batch"], 2)
        self.assertEqual(response.json["siteGrp"], 2)
        self.assertEqual(response.json["finalCodeID"], 2)
        self.assertEqual(response.json["finalCodeDate"], "2016-02-03")
        self.assertEqual(response.json["enrollmentDate"], "2016-02-03")
        self.assertEqual(response.json["dateCoordSigned"], "2016-02-03")
        self.assertEqual(response.json["importDate"], "2016-02-03")
        self.assertEqual(response.json["finalCodeStaffID"], 2)
        self.assertEqual(response.json["enrollmentStaffID"], 2)
        self.assertEqual(response.json["abstractStatusID"], 2)
        self.assertEqual(response.json["abstractStatusDate"], "2016-02-03")
        self.assertEqual(response.json["abstractStatusStaffID"], 2)
        self.assertEqual(response.json["sentToAbstractorDate"], "2016-02-03")
        self.assertEqual(response.json["sentToAbstractorStaffID"], 2)
        self.assertEqual(response.json["abstractedDate"], "2016-02-03")
        self.assertEqual(response.json["abstractorStaffID"], 2)
        self.assertEqual(response.json["researcherDate"], "2016-02-03")
        self.assertEqual(response.json["researcherStaffID"], 2)
        self.assertEqual(response.json["consentLink"], "link Updated")
        self.assertEqual(response.json["medRecordReleaseSigned"], False)
        self.assertEqual(response.json["medRecordReleaseLink"], "link Updated")
        self.assertEqual(response.json["medRecordReleaseStaffID"], 2)
        self.assertEqual(response.json["medRecordReleaseDate"], "2016-02-03")
        self.assertEqual(response.json["surveyToResearcher"], "2016-02-03")
        self.assertEqual(response.json["surveyToResearcherStaffID"], 2)
        self.assertEqual(response.json["qualityControl"], False)
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_project_patient(self):
        response = self.client.delete("/api/projectpatients/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ParticipantID 2 deleted")

    def test_delete_project_patient2(self):
        response = self.client.delete("/api/projectpatients/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestProjectStaff(PopulatedDB):
    def test_get_staffs(self):
        response = self.client.get("/api/projectstaff/")
        self.assertEqual(response.json["ProjectStaff"][0]["staffRoleID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["datePledge"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["dateRevoked"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["contactID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["inactiveID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["versionID"], 1)

    def test_get_staff(self):
        response = self.client.get("/api/projectstaff/1/")
        self.assertEqual(response.json["staffRoleID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["datePledge"], "2016-02-02")
        self.assertEqual(response.json["dateRevoked"], "2016-02-02")
        self.assertEqual(response.json["contactID"], 1)
        self.assertEqual(response.json["inactiveID"], 1)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_staff(self):
        response = self.client.put("/api/projectstaff/1/", data = {
            "staffRoleID" : 2,
            "projectID" : 2,
            "staffID" : 2,
            "datePledge" : "2016-02-03",
            "dateRevoked" : "2016-02-03",
            "contactID" : 2,
            "inactiveID" : 2,
            "versionID" : 1
        })
        self.assertEqual(response.json["staffRoleID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["datePledge"], "2016-02-03")
        self.assertEqual(response.json["dateRevoked"], "2016-02-03")
        self.assertEqual(response.json["contactID"], 2)
        self.assertEqual(response.json["inactiveID"], 2)
        self.assertEqual(response.json["versionID"], 2)

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
        self.assertEqual(response.json["ProjectStatuses"][0]["versionID"], 1)

    def test_get_project_status(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json["projectStatusID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["statusDate"], "2016-02-02")
        self.assertEqual(response.json["statusNotes"], "notes")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_project_status(self):
        response = self.client.put("/api/projectstatuses/1/", data = {
            "projectStatusTypeID" : 2,
            "projectID": 2,
            "staffID" : 2,
            "statusDate" : "2016-02-03",
            "statusNotes": "notes Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["projectStatusTypeID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["statusDate"], "2016-02-03")
        self.assertEqual(response.json["statusNotes"], "notes Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_project_status(self):
        response = self.client.delete("/api/projectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusID 1 deleted")

class TestProjectStatusType(PopulatedDB):
    def test_get_project_status_types(self):
        response = self.client.get("/api/projectstatustypes/")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatusTypeID"], 1)
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatus"], "Pending")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatusDefinition"], "Project has not started")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["versionID"], 1)

    def test_get_project_status_type(self):
        response = self.client.get("/api/projectstatustypes/1/")
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["projectStatus"], "Pending")
        self.assertEqual(response.json["projectStatusDefinition"], "Project has not started")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_project_status_type(self):
        response = self.client.put("/api/projectstatustypes/1/", data = {
            "projectStatus" : "Status 1 Updated",
            "projectStatusDefinition" : "status def Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["projectStatus"], "Status 1 Updated")
        self.assertEqual(response.json["projectStatusDefinition"], "status def Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_project_status_type(self):
        response = self.client.delete("/api/projectstatustypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusTypeID 2 deleted")

    def test_delete_project_status_type2(self):
        response = self.client.delete("/api/projectstatustypes/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestProjectType(PopulatedDB):
    def test_get_project_types(self):
        response = self.client.get("/api/projecttypes/")
        self.assertEqual(response.json["ProjectTypes"][0]["projectType"], "Consent")
        self.assertEqual(response.json["ProjectTypes"][0]["projectTypeDefinition"], "UCR obtains patient consent for project")
        self.assertEqual(response.json["ProjectTypes"][0]["versionID"], 1)

    def test_get_project_type(self):
        response = self.client.get("/api/projecttypes/1/")
        self.assertEqual(response.json["projectType"], "Consent")
        self.assertEqual(response.json["projectTypeDefinition"], "UCR obtains patient consent for project")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_project_type(self):
        response = self.client.put("/api/projecttypes/1/", data = {
            "projectType" : "type updated",
            "projectTypeDefinition" : "type def Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["projectType"], "type updated")
        self.assertEqual(response.json["projectTypeDefinition"], "type def Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_project_type(self):
        response = self.client.delete("/api/projecttypes/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectTypeID 2 deleted")

    def test_delete_project_type2(self):
        response = self.client.delete("/api/projecttypes/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestReviewCommitteeStatusLUT(PopulatedDB):
    def test_get_rcStatusList(self):
        response = self.client.get("/api/reviewcommitteestatuses/")
        self.assertEqual(response.json["ReviewCommitteeStatuses"][0]["reviewCommitteeStatusID"], 1)
        self.assertEqual(response.json["ReviewCommitteeStatuses"][0]["reviewCommitteeStatus"], "Pending")
        self.assertEqual(response.json["ReviewCommitteeStatuses"][0]["reviewCommitteeStatusDefinition"], "Pending")
        self.assertEqual(response.json["ReviewCommitteeStatuses"][0]["versionID"], 1)

    def test_get_rcStatus(self):
        response = self.client.get("/api/reviewcommitteestatuses/1/")
        self.assertEqual(response.json["reviewCommitteeStatusID"], 1)
        self.assertEqual(response.json["reviewCommitteeStatus"], "Pending")
        self.assertEqual(response.json["reviewCommitteeStatusDefinition"], "Pending")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_rcStatus(self):
        response = self.client.put("/api/reviewcommitteestatuses/1/", data = {
            "reviewCommitteeStatus" : "Status 1 Updated",
            "reviewCommitteeStatusDefinition" : "rc status def Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["reviewCommitteeStatusID"], 1)
        self.assertEqual(response.json["reviewCommitteeStatus"], "Status 1 Updated")
        self.assertEqual(response.json["reviewCommitteeStatusDefinition"], "rc status def Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_rcStatusList(self):
        response = self.client.delete("/api/reviewcommitteestatuses/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ReviewCommitteeStatusID 2 deleted")

    def test_delete_rcStatusList2(self):
        response = self.client.delete("/api/reviewcommitteestatuses/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestReviewCommittee(PopulatedDB):
    def test_get_review_committees(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json['reviewCommittees'][0]["projectID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["reviewCommitteeStatusID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["reviewCommitteeLUTID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["reviewCommitteeNumber"], "1")
        self.assertEqual(response.json['reviewCommittees'][0]["dateInitialReview"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["dateExpires"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["rcNote"], "rc_note")
        self.assertEqual(response.json['reviewCommittees'][0]["rcProtocol"], "rc_proto")
        self.assertEqual(response.json['reviewCommittees'][0]["rcApproval"], "rc_approval")
        self.assertEqual(response.json['reviewCommittees'][0]["versionID"], 1)

    def test_get_review_committee(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["reviewCommitteeStatusID"], 1)
        self.assertEqual(response.json["reviewCommitteeLUTID"], 1)
        self.assertEqual(response.json["reviewCommitteeNumber"], "1")
        self.assertEqual(response.json["dateInitialReview"], "2016-02-02")
        self.assertEqual(response.json["dateExpires"], "2016-02-02")
        self.assertEqual(response.json["rcNote"], "rc_note")
        self.assertEqual(response.json["rcProtocol"], "rc_proto")
        self.assertEqual(response.json["rcApproval"], "rc_approval")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommittees/1/", data = {
            "projectID" : 2,
            "reviewCommitteeStatusID": 2,
            "reviewCommitteeLUTID": 2,
            "reviewCommitteeNumber":"2",
            "dateInitialReview":"2016-02-03",
            "dateExpires" : "2016-02-03",
            "rcNote" : "rc_note Updated",
            "rcProtocol" : "rc_proto Updated",
            "rcApproval":"rc_approval Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["reviewCommitteeStatusID"], 2)
        self.assertEqual(response.json["reviewCommitteeLUTID"], 2)
        self.assertEqual(response.json["reviewCommitteeNumber"], "2")
        self.assertEqual(response.json["dateInitialReview"], "2016-02-03")
        self.assertEqual(response.json["dateExpires"], "2016-02-03")
        self.assertEqual(response.json["rcNote"], "rc_note Updated")
        self.assertEqual(response.json["rcProtocol"], "rc_proto Updated")
        self.assertEqual(response.json["rcApproval"], "rc_approval Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_review_committee(self):
        response = self.client.delete("/api/reviewcommittees/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ReviewCommitteeID 1 deleted")

class TestReviewCommitteeLUT(PopulatedDB):
    def test_get_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json["ReviewCommitteeList"][0]["reviewCommittee"], "U of U IRB")
        self.assertEqual(response.json["ReviewCommitteeList"][0]["reviewCommitteeDescription"], None)
        self.assertEqual(response.json["ReviewCommitteeList"][0]["versionID"], 1)

    def test_get_review_committee_list(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["reviewCommittee"], "U of U IRB")
        self.assertEqual(response.json["reviewCommitteeDescription"], None)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommitteelist/1/", data = {
            "reviewCommittee" : "rc Updated",
            "reviewCommitteeDescription" : "rc desc Updated",
            "versionID" : 1
            })
        self.assertEqual(response.json["reviewCommittee"],"rc Updated")
        self.assertEqual(response.json["reviewCommitteeDescription"],"rc desc Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_review_committee_list(self):
        response = self.client.delete("/api/reviewcommitteelist/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ReviewCommitteeID 2 deleted")


    def test_delete_review_committee_list2(self):
        response = self.client.delete("/api/reviewcommitteelist/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestStaff(PopulatedDB):
    def test_get_staffs(self):
        response = self.client.get("/api/staff/")
        self.assertEqual(response.json["Staff"][0]["userID"], 1)
        self.assertEqual(response.json["Staff"][0]["staffID"], 1)
        self.assertEqual(response.json["Staff"][0]["firstName"], "Aaron")
        self.assertEqual(response.json["Staff"][0]["lastName"], "Thomas")
        self.assertEqual(response.json["Staff"][0]["middleName"], "Pulver")
        self.assertEqual(response.json["Staff"][0]["email"], "aaron.pulver@utah.edu")
        self.assertEqual(response.json["Staff"][0]["phoneNumber"], "phone")
        self.assertEqual(response.json["Staff"][0]["phoneComment"], "phoneComment")
        self.assertEqual(response.json["Staff"][0]["institution"], "institution")
        self.assertEqual(response.json["Staff"][0]["department"], "department")
        self.assertEqual(response.json["Staff"][0]["position"], "position")
        self.assertEqual(response.json["Staff"][0]["credentials"], "credentials")
        self.assertEqual(response.json["Staff"][0]["street"], "street")
        self.assertEqual(response.json["Staff"][0]["city"], "city")
        self.assertEqual(response.json["Staff"][0]["stateID"], 1)
        self.assertEqual(response.json["Staff"][0]["ucrRoleID"], 1)
        self.assertEqual(response.json["Staff"][0]["versionID"], 1)

    def test_get_staff(self):
        response = self.client.get("/api/staff/1/")
        self.assertEqual(response.json["userID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["firstName"], "Aaron")
        self.assertEqual(response.json["lastName"], "Thomas")
        self.assertEqual(response.json["middleName"], "Pulver")
        self.assertEqual(response.json["email"], "aaron.pulver@utah.edu")
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneComment"], "phoneComment")
        self.assertEqual(response.json["institution"], "institution")
        self.assertEqual(response.json["department"], "department")
        self.assertEqual(response.json["position"], "position")
        self.assertEqual(response.json["credentials"], "credentials")
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["stateID"], 1)
        self.assertEqual(response.json["ucrRoleID"], 1)
        self.assertEqual(response.json["versionID"], 1)

    def test_update_staff(self):
        response = self.client.put("/api/staff/1/", data = {
            "userID": 2,
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
            "stateID" : 2,
            "ucrRoleID" : 2,
            "versionID" : 1
            })
        # Don't update userID
        self.assertEqual(response.json["userID"], 1)
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
        self.assertEqual(response.json["stateID"], 2)
        self.assertEqual(response.json["ucrRoleID"], 2)
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_staff(self):
        response = self.client.delete("/api/staff/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffID 2 deleted")

    def test_delete_staff2(self):
        response = self.client.delete("/api/staff/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestStaffRole(PopulatedDB):
    def test_get_staff_roles(self):
        response = self.client.get("/api/staffroles/")
        self.assertEqual(response.json["StaffRoles"][0]["staffRoleID"], 1)
        self.assertEqual(response.json["StaffRoles"][0]["staffRole"], "PI-External")
        self.assertEqual(response.json["StaffRoles"][0]["staffRoleDescription"], "Principle Investigator- external, no U of U affiliation")
        self.assertEqual(response.json["StaffRoles"][0]["versionID"], 1)

    def test_get_staff_role(self):
        response = self.client.get("/api/staffroles/1/")
        self.assertEqual(response.json["staffRoleID"], 1)
        self.assertEqual(response.json["staffRole"], "PI-External")
        self.assertEqual(response.json["staffRoleDescription"], "Principle Investigator- external, no U of U affiliation")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_staff_role(self):
        response = self.client.put("/api/staffroles/1/", data = {
            "staffRole" : "role Updated",
            "staffRoleDescription" : "desc Updated",
            "versionID" : 1
            })
        self.assertEqual(response.json["staffRoleID"], 1)
        self.assertEqual(response.json["staffRole"], "role Updated")
        self.assertEqual(response.json["staffRoleDescription"], "desc Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_staff_role(self):
        response = self.client.delete("/api/staffroles/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffRoleID 2 deleted")

    def test_delete_staff_role2(self):
        response = self.client.delete("/api/staffroles/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestStaffTraining(PopulatedDB):
    def test_get_staff_trainings(self):
        response = self.client.get("/api/stafftrainings/")
        self.assertEqual(response.json["StaffTrainings"][0]["staffTrainingID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["staffID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["dateTaken"], "2016-02-02")
        self.assertEqual(response.json["StaffTrainings"][0]["dateExpires"], "2016-02-02")
        self.assertEqual(response.json["StaffTrainings"][0]["versionID"], 1)

    def test_get_staff_training(self):
        response = self.client.get("/api/stafftrainings/1/")
        self.assertEqual(response.json["staffTrainingID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["dateTaken"], "2016-02-02")
        self.assertEqual(response.json["dateExpires"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_staff_training(self):
        response = self.client.put("/api/stafftrainings/1/", data = {
            "staffID" : 2,
            "humanSubjectTrainingID" : 2,
            "dateTaken" : "2016-02-03",
            "dateExpires" : "2016-02-03",
            "versionID" : 1
            })
        self.assertEqual(response.json["staffTrainingID"], 1)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["humanSubjectTrainingID"], 2)
        self.assertEqual(response.json["dateTaken"], "2016-02-03")
        self.assertEqual(response.json["dateExpires"], "2016-02-03")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_staff_training(self):
        response = self.client.delete("/api/stafftrainings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffTrainingID 1 deleted")

class TestTracing(PopulatedDB):
    def test_get_tracings(self):
        response = self.client.get("/api/tracings/")
        self.assertEqual(response.json["Tracings"][0]["tracingID"], 1)
        self.assertEqual(response.json["Tracings"][0]["tracingSourceID"], 1)
        self.assertEqual(response.json["Tracings"][0]["participantID"], 1)
        self.assertEqual(response.json["Tracings"][0]["date"], "2016-02-02")
        self.assertEqual(response.json["Tracings"][0]["staffID"], 1)
        self.assertEqual(response.json["Tracings"][0]["notes"], "notes")
        self.assertEqual(response.json["Tracings"][0]["versionID"], 1)

    def test_get_tracing(self):
        response = self.client.get("/api/tracings/1/")
        self.assertEqual(response.json["tracingID"], 1)
        self.assertEqual(response.json["tracingSourceID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["date"], "2016-02-02")
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["notes"], "notes")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_tracing(self):
        response = self.client.put("/api/tracings/1/", data = {
            "tracingSourceID" : 2,
            "participantID" : 2,
            "date" : "2016-02-03",
            "staffID" : 2,
            "notes" : "notes Updated",
            "versionID" : 1
            })
        self.assertEqual(response.json["tracingID"], 1)
        self.assertEqual(response.json["tracingSourceID"], 2)
        self.assertEqual(response.json["participantID"], 2)
        self.assertEqual(response.json["date"], "2016-02-03")
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["notes"], "notes Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_tracing(self):
        response = self.client.delete("/api/tracings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "TracingID 1 deleted")

class TestTracingSource(PopulatedDB):
    def test_get_tracing_sources(self):
        response = self.client.get("/api/tracingsources/")
        self.assertEqual(response.json["TracingSources"][0]["tracingSourceID"], 1)
        self.assertEqual(response.json["TracingSources"][0]["description"], "DMS")
        self.assertEqual(response.json["TracingSources"][0]["versionID"], 1)

    def test_get_tracing_source(self):
        response = self.client.get("/api/tracingsources/1/")
        self.assertEqual(response.json["tracingSourceID"], 1)
        self.assertEqual(response.json["description"], "DMS")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_tracing_source(self):
        response = self.client.put("/api/tracingsources/1/", data = {
            "description" : "desc Updated",
            "versionID" : 1
            })
        self.assertEqual(response.json["tracingSourceID"], 1)
        self.assertEqual(response.json["description"], "desc Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_tracing_source(self):
        response = self.client.delete("/api/tracingsources/2/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "TracingSourceID 2 deleted")

    def test_delete_tracing_source2(self):
        response = self.client.delete("/api/tracingsources/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")

class TestUCRReport(PopulatedDB):
    def test_get_ucr_reports(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json["ucrReports"][0]["projectID"],1)
        self.assertEqual(response.json["ucrReports"][0]["reportTypeID"],1)
        self.assertEqual(response.json["ucrReports"][0]["reportSubmitted"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["reportDue"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["reportDoc"],"doc")
        self.assertEqual(response.json["ucrReports"][0]["versionID"], 1)

    def test_get_ucr_report(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["reportTypeID"],1)
        self.assertEqual(response.json["reportSubmitted"],"2016-02-02")
        self.assertEqual(response.json["reportDue"],"2016-02-02")
        self.assertEqual(response.json["reportDoc"],"doc")
        self.assertEqual(response.json["versionID"], 1)

    def test_update_ucr_report(self):
        response = self.client.put("/api/ucrreports/1/", data = {
            "projectID" : 2,
            "reportTypeID": 2,
            "reportSubmitted": "2016-02-03",
            "reportDue": "2016-02-03",
            "reportDoc": "doc Updated",
            "versionID" : 1
        })
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["reportTypeID"],2)
        self.assertEqual(response.json["reportSubmitted"],"2016-02-03")
        self.assertEqual(response.json["reportDue"],"2016-02-03")
        self.assertEqual(response.json["reportDoc"],"doc Updated")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_ucr_report(self):
        response = self.client.delete("/api/ucrreports/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "UcrReportID 1 deleted")

class TestUCRRole(PopulatedDB):

    def test_get_ucr_role(self):
        response = self.client.get("/api/ucrroles/1/")
        self.assertEqual(response.json["ucrRoleID"],1)
        self.assertEqual(response.json["ucrRole"],"role 1")
        self.assertEqual(response.json["versionID"],1)

    def test_get_ucr_roles(self):
        response = self.client.get("/api/ucrroles/")
        self.assertEqual(response.json["ucrRoles"][0]["ucrRoleID"], 1)
        self.assertEqual(response.json["ucrRoles"][0]["ucrRole"], "role 1")
        self.assertEqual(response.json["ucrRoles"][0]["versionID"], 1)

    def test_update_ucr_role(self):
        response = self.client.put("/api/ucrroles/1/", data={
            "ucrRole": "role 2",
            "versionID": 1
        })
        self.assertEqual(response.json["ucrRoleID"], 1)
        self.assertEqual(response.json["ucrRole"], "role 2")
        self.assertEqual(response.json["versionID"], 2)

    def test_delete_ucr_role(self):
        response = self.client.delete("/api/ucrroles/2/")
        self.assertEqual(response.json["Message"], "UCRRoleID 2 deleted")

    def test_delete_ucr_role2(self):
        response = self.client.delete("/api/ucrroles/1/")
        
        self.assertEqual(response.json["Message"], "Dependency Detected")
        
if __name__ == '__main__':
    unittest.main()