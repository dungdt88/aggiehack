<?php

namespace Csg\DataBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Class DefaultController
 * @package Csg\DemoBundle\Command
 */
class DefaultController extends Controller
{
    /**
     * @return Response
     */
    public function indexAction()
    {
        die('asdasd');
        return $this->render('CsgDemoBundle:Default:index.html.twig');
    }

    
}
