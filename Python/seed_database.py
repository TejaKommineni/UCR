"""
    This is a stand-a-lone script that can seed the database for ad-hoc testing
"""

from flask import Flask
import app
from app.database import db
from datetime import datetime
import app.models as models


def create_final_codes():
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


def create_states():
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


def create_abstract_statuses():
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


def create_sexes():
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


def create_races():
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


def create_ethnicities():
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


def create_vital_statuses():
    vitals = []
    vitals.append(models.VitalStatus(
        vitalStatus="Alive"
    ))
    vitals.append(models.VitalStatus(
        vitalStatus="Dead"
    ))
    return vitals


def create_contacts():
    contacts = []
    contacts.append(models.Contacts(
        contact="yes"
    ))
    contacts.append(models.Contacts(
        contact="no"
    ))
    return contacts


def create_inactives():
    inactives = []
    inactives.append(models.Inactive(
        inactive="Yes"
    ))
    inactives.append(models.Inactive(
        inactive="No"
    ))
    return inactives


def create_ucr_report_types():
    reports = []
    reports.append(models.UCRReportType(
        ucrReportType="Report 1"
    ))
    reports.append(models.UCRReportType(
        ucrReportType="Report 2"
    ))
    return reports


def create_physician_statuses():
    statuses = []
    statuses.append(models.PhysicianStatus(
        physicianStatus="active"
    ))
    statuses.append(models.PhysicianStatus(
        physicianStatus="inactive"
    ))
    return statuses


def create_physician_facility_statuses():
    statuses = []
    statuses.append(models.PhysicianFacilityStatus(
        physicianFacilityStatus="open"
    ))
    statuses.append(models.PhysicianFacilityStatus(
        physicianFacilityStatus="closed"
    ))
    return statuses


def create_phone_types():
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


def create_irb_holders():
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


def create_project_types():
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


def create_contact_statuses():
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


def create_contact_sources():
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


def create_grant_statuses():
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


def create_funding_sources():
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


def create_review_committee_statuses():
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


def create_project_statuses():
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


def create_log_subjects():
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


def create_review_committees():
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


def create_staff_roles():
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


def create_project_phases():
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


def create_human_subject_trainings():
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


def create_tracing_sources():
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


def create_contact_types():
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


def create_ucr_roles():
    roles = []
    roles.append(models.UCRRole(
        ucrRole="role 1"
    ))
    roles.append(models.UCRRole(
        ucrRole="role 2"
    ))
    return roles


def create_gift_cards():
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


def create_roles():
    roles = []
    roles.append(models.Role(
        role="Contact Staff"
    ))
    roles.append(models.Role(
        role="Developer"
    ))
    roles.append(models.Role(
        role="Director"
    ))
    roles.append(models.Role(
        role="Informatics Staff"
    ))
    roles.append(models.Role(
        role="Research Manager"
    ))
    return roles


def create_users():
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


def populate_db():
    """
    This creates the database/tables and populates it with junk data for testing
    :return:
    """
    db.drop_all()
    db.create_all()

    roles = create_roles()
    users = create_users()
    finalCodes = create_final_codes()
    states = create_states()
    abstractStatuses = create_abstract_statuses()
    sexes = create_sexes()
    races = create_races()
    ethnicities = create_ethnicities()
    vitals = create_vital_statuses()
    contacts = create_contacts()
    inactives = create_inactives()
    ucrReportTypes = create_ucr_report_types()
    physicianStatuses = create_physician_statuses()
    physFacilityStatuses = create_physician_facility_statuses()
    phoneTypes = create_phone_types()
    irbHolders = create_irb_holders()
    projectTypes = create_project_types()
    contactStatuses = create_contact_statuses()
    contactSources = create_contact_sources()
    grantStatuses = create_grant_statuses()
    fundingSources = create_funding_sources()
    reviewCommitteeStatuses = create_review_committee_statuses()
    projectStatuses = create_project_statuses()
    logTypes = create_log_subjects()
    reviewCommittees = create_review_committees()
    staffRoles = create_staff_roles()
    projectPhases = create_project_phases()
    hsts = create_human_subject_trainings()
    tracingSources = create_tracing_sources()
    contactTypes = create_contact_types()
    ucrRoles = create_ucr_roles()
    giftCards = create_gift_cards()

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
        informantPrimary="informant_primary",
        informantRelationship="informant_relationship",
        notes="notes"
    )
    informant2 = models.Informant(
        participantID=1,
        firstName="fname",
        lastName="lname",
        middleName="middle_name",
        informantPrimary="informant_primary",
        informantRelationship="informant_relationship",
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
    db.session.add_all(roles)
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
    db.session.add_all(ucrRoles)
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


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app("config.py").app_context().push()
    populate_db()
    print("Seeded Database")