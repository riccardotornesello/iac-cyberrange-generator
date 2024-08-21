terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "cyberrange" {
  name     = "cyberrange"
  location = "West Europe"
}

resource "azurerm_virtual_network" "cyberrange" {
  name                = "cyberrange"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.cyberrange.location
  resource_group_name = azurerm_resource_group.cyberrange.name
}

resource "azurerm_subnet" "main" {
  name                 = "main"
  resource_group_name  = azurerm_resource_group.cyberrange.name
  virtual_network_name = azurerm_virtual_network.cyberrange.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_interface" "manager" {
  name                = "manager-nic"
  location            = azurerm_resource_group.cyberrange.location
  resource_group_name = azurerm_resource_group.cyberrange.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.0.1.5"
  }
}

resource "azurerm_virtual_machine" "manager" {
  name                  = "manager-vm"
  location              = azurerm_resource_group.cyberrange.location
  resource_group_name   = azurerm_resource_group.cyberrange.name
  network_interface_ids = [azurerm_network_interface.manager.id]
  vm_size               = "Standard_B1s"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "manager-os-disk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "manager"
    admin_username = "testadmin"
    admin_password = "testAdmin1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}