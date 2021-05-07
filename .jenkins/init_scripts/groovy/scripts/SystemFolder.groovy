// Initializes the python_resume jobs directory, which runs with deployed scripts and repos

import com.cloudbees.hudson.plugins.folder.Folder
import com.synopsys.arc.jenkins.plugins.ownership.OwnershipDescription
import com.synopsys.arc.jenkins.plugins.ownership.jobs.JobOwnerHelper
import hudson.plugins.git.GitSCM
import jenkins.model.Jenkins
import jenkins.plugins.git.GitSCMSource
import org.jenkinsci.plugins.ownership.model.folders.FolderOwnershipHelper
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import org.jenkinsci.plugins.workflow.libs.FolderLibraries
import org.jenkinsci.plugins.workflow.libs.LibraryConfiguration
import org.jenkinsci.plugins.workflow.libs.SCMSourceRetriever
import org.jenkinsci.plugins.workflow.job.WorkflowJob

println("=== Initialize the Python_Resume folder")
if (Jenkins.instance.getItem("Python_Resume") != null) {
    println("Python_Resume folder has been already initialized, skipping the step")
    return
}

def folder = Jenkins.instance.createProject(Folder.class, "Python_Resume")

// Include https://github.com/jenkins-infra/pipeline-library
def pipelineLibrarySource = new GitSCMSource("pipeline-library", "https://github.com/jenkins-infra/pipeline-library.git", null, null, null, false)
LibraryConfiguration lc = new LibraryConfiguration("pipeline-library", new SCMSourceRetriever(pipelineLibrarySource))
lc.with {
    implicit = true
    defaultVersion = "master"
}
folder.addProperty(new FolderLibraries([lc]))
FolderOwnershipHelper.setOwnership(folder, new OwnershipDescription(true, "admin"))

WorkflowJob project1 = folder.createProject(WorkflowJob.class, "Unit_Test")
project1.setDefinition(new CpsFlowDefinition("buildPlugin(platforms: ['master'], repo: 'https://github.com/jondkelley/python_resume.git')", true))
JobOwnerHelper.setOwnership(project1, new OwnershipDescription(true, "admin", Arrays.asList("user")))


