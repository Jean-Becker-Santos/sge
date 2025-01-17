from django.core.management.base import BaseCommand
from inflows.models import Inflow
from products.models import Product
from suppliers.models import Supplier
import csv


class Command(BaseCommand):
    help = 'Importa dados de inflow a partir de um arquivo CSV, buscando produto de forma case-insensitive.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com inflows',
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            # Ajuste o 'delimiter' conforme necessário (',' ou ';')
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:
                produto_original = row['produto']  # valor que vem cru do CSV
                fornecedor = row['fornecedor']
                descricao = row['descricao']
                quantidade = int(row['quantidade'])

                # Remove espaços extras no início e final
                produto_limpo = produto_original.strip()
                
                # Tenta primeiro buscar de forma exata, mas ignorando maiúsculo/minúsculo
                product_obj = Product.objects.filter(title__iexact=produto_limpo).first()

                if not product_obj:
                    # Se não encontrar, tenta achar um "aproximado" (que contenha a string)
                    product_obj = Product.objects.filter(title__icontains=produto_limpo).first()

                if not product_obj:
                    self.stdout.write(self.style.ERROR(
                        f'Produto "{produto_original}" não encontrado. Verifique seu CSV.'
                    ))
                    continue
                
                # Agora busca o fornecedor (ignora, se quiser, caso-insensitive também)
                fornecedor_limpo = fornecedor.strip()
                supplier_obj = Supplier.objects.filter(name__iexact=fornecedor_limpo).first()

                if not supplier_obj:
                    self.stdout.write(self.style.ERROR(
                        f'Fornecedor "{fornecedor}" não encontrado. Verifique seu CSV.'
                    ))
                    continue

                # Cria o Inflow
                inflow = Inflow.objects.create(
                    product=product_obj,
                    supplier=supplier_obj,
                    quantity=quantidade,
                    description=descricao
                )

                self.stdout.write(self.style.NOTICE(
                    f'Inflow criado com sucesso: {inflow.product} ({inflow.quantity})'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            'Importação de Inflows concluída com sucesso!'
        ))
