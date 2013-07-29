from drozer.modules import common, Module

class Check(Module, common.VulnerabilityScanner):

    name = "Test for vulnerabilities that allow a malicious application to gain root access."
    description = "Test for vulnerabilities that allow a malicious application to gain root access."
    examples = ""
    author = ["Tyrone (@mwrlabs)"]
    date = "2013-01-14"
    license = "BSD (3 clause)"
    path = ["scanner", "root"]

    vulnerabilities = "exploit.root."
    
