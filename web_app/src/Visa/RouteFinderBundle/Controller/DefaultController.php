<?php

namespace Visa\RouteFinderBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    public function indexAction()
    {
        return $this->render('VisaRouteFinderBundle:Default:index.html.twig');
    }
}
