import stripe
from django.conf import settings  # alterar settings quando for upar no heroku
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.views import View
from django.views.generic import TemplateView
from .models import Produto
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


def base(request):
    return render(request, 'base.html')


class SucessoView(TemplateView):
    template_name = 'sucesso.html'


class CanceladoView(TemplateView):
    template_name = 'cancelado.html'


class index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        produto = Produto.objects.get(nome="Tênis Nike Air Max 97")
        context = super(index, self).get_context_data(**kwargs)
        context.update({
            "produto": produto,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        produto_id = self.kwargs["pk"]
        produto = Produto.objects.get(id=produto_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'unit_amount': produto.preco,
                        'product_data': {
                            'name': produto.nome,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'], descomentar caso queria adicionar imagem do produto no checkout
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "produto_id": produto.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/',
            cancel_url=YOUR_DOMAIN + '/',
        )
        messages.success(request, f'Compra realizada com sucesso. Você receberá mais informações no e-mail informado na compra.')
        return JsonResponse({
            'id': checkout_session.id
        })
        
@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        
        session = event['data']['object']
        
        print(session)

        customer_email = session["customer_details"]["email"]
        produto_id = session["metadata"]["produto_id"]

        produto = Produto.objects.get(id=produto_id)

        send_mail(
            subject="Aqui está o seu produto !",
            message="Obrigado por comprar nosso produto e colaborar com a comunidade de desenvolvimento =)",
            recipient_list=[customer_email],
            from_email="python-store@gmail.com"
        )
    # Passed signature verification
    return HttpResponse(status=200)
