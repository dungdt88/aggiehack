<?php

namespace Visa\DemoBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    public function indexAction()
    {
        return $this->render('VisaDemoBundle:Default:index.html.twig');
    }
}
