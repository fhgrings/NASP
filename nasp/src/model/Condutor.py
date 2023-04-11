# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 18:25:59 2019

@author: Cristian
"""
from ..database.HyberGrings import HyberGrings

#%%

class Condutor(HyberGrings):
    
    def __init__(self,dados=None):
        self.__CPF_condutor = None
        self.__nome   = None
        self.__Telefone    = None
        self.__Data_cadastro       = None
        super(Condutor, self).__init__(self.__class__.__name__, self.__dict__)
        if dados:
            self.fromTuple(dados)

    
    @property
    def CPF_condutor(self):
        return self.__CPF_condutor
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self,nome):
        self.__nome = nome
        self.update()

    @property
    def Telefone(self):
        return self.__Telefone
    
    @Telefone.setter
    def Telefone(self,Telefone):
        self.__Telefone = Telefone
        self.update()
    
    @property
    def Data_cadastro(self):
        return self.__Data_cadastro
    
    @Data_cadastro.setter
    def Data_cadastro(self,Data_cadastro):
        self.__Data_cadastro = Data_cadastro
        self.update()
    
    def __str__(self):
        return "{"+f"""
        "CPF_condutor":\t"{self.__CPF_condutor}",
        "nome":\t"{self.__nome}",
        "telefone":\t"{self.__Telefone}",
        "data_cadastro":\t"{self.__Data_cadastro}" """"}"
