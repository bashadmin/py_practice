import sys
import boto3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QMessageBox

# Create VPC Wizard class
class VpcWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPC Wizard")
        self.setGeometry(100, 100, 200, 200)

        # Create buttons
        self.public_subnet_btn = QPushButton("Create VPC", self)
        self.public_subnet_btn.move(20, 20)
        self.public_subnet_btn.clicked.connect(self.create_public_subnet_vpc)

        # Create close button
        self.close_btn = QPushButton("Close", self)
        self.close_btn.move(20, 80)
        self.close_btn.clicked.connect(self.close)

        # Initialize Boto3 client with region
        self.ec2 = boto3.client('ec2', region_name='us-west-2')

    # Create VPC with a single public subnet
    def create_public_subnet_vpc(self):
        # Get VPC configuration options from user
        vpc_name, vpc_cidr, subnet_cidr = self.get_vpc_config()

        try:
            # Create VPC
            vpc = self.ec2.create_vpc(CidrBlock=vpc_cidr)

            # Add name tag to VPC
            self.ec2.create_tags(Resources=[vpc['Vpc']['VpcId']], Tags=[{'Key': 'Name', 'Value': vpc_name}])

            # Create internet gateway
            igw = self.ec2.create_internet_gateway()

            # Attach internet gateway to VPC
            self.ec2.attach_internet_gateway(InternetGatewayId=igw['InternetGateway']['InternetGatewayId'], VpcId=vpc['Vpc']['VpcId'])

            # Create public subnet
            subnet = self.ec2.create_subnet(VpcId=vpc['Vpc']['VpcId'], CidrBlock=subnet_cidr)

            # Create route table
            route_table = self.ec2.create_route_table(VpcId=vpc['Vpc']['VpcId'])

            # Create route for internet traffic
            self.ec2.create_route(RouteTableId=route_table['RouteTable']['RouteTableId'], DestinationCidrBlock='0.0.0.0/0', GatewayId=igw['InternetGateway']['InternetGatewayId'])

            # Associate route table with subnet
            self.ec2.associate_route_table(RouteTableId=route_table['RouteTable']['RouteTableId'], SubnetId=subnet['Subnet']['SubnetId'])

            QMessageBox.information(self, "VPC Creation Successful", "Amazon VPC with a single public subnet has been created successfully!")
        except Exception as e:
            QMessageBox.critical(self, "VPC Creation Failed", f"An error occurred while creating the VPC: {str(e)}")

    # Get VPC configuration options from user
    def get_vpc_config(self):
        vpc_name, ok = QInputDialog.getText(self, "VPC Configuration", "Enter VPC name:")
        if not ok:
            return None, None, None
        vpc_cidr, ok = QInputDialog.getText(self, "VPC Configuration", "Enter VPC CIDR block (e.g. 10.0.0.0/16):")
        if not ok:
            return None, None, None
        subnet_cidr, ok = QInputDialog.getText(self, "VPC Configuration", "Enter subnet CIDR block (e.g. 10.0.0.0/24):")
        if not ok:
            return None, None, None
        return vpc_name, vpc_cidr, subnet_cidr

if __name__ == "__main__":
    # Initialize PyQt application
    app = QApplication(sys.argv)
    
    # Create instance of VpcWizard
    vpc_wizard = VpcWizard()
    vpc_wizard.show()

    # Close application when window is closed
    sys.exit(app.exec_())